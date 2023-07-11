import datetime
import decimal
import random

from django.db.models import Avg, QuerySet

from .models import ActiveAlert, ProductPriceLog


def gather_price_change_insight(
    tracked_products: QuerySet,
    average_price_by_product_id: dict,
    lookback_days: int,
    alert: ActiveAlert,
) -> dict:
    """
    Gathers insights about the percentage price change from the
    average price of products over the specified lookback days.

    :param tracked_products: QuerySet of ProductPriceLog objects
    :param average_price_by_product_id: dict of product id to average price
    :param lookback_days: number of days to look back for price changes
    :alert: ActiveAlert instance to extract user email
    """
    # Calculate percentage change in price from average price
    products_by_percentage_change_in_price = []
    for product in tracked_products:
        current_price = product.price
        average_price = average_price_by_product_id.get(product.item_id)
        if average_price:
            percentage_change_in_price_from_avg = (
                (current_price - average_price) / average_price
            ) * 100
            products_by_percentage_change_in_price.append(
                {
                    "product": product,
                    "percentage_change_in_price": percentage_change_in_price_from_avg,
                }
            )

    # Pick a random product from the list
    random_index = random.randint(0, len(products_by_percentage_change_in_price) - 1)
    product_chosen_for_insight = products_by_percentage_change_in_price[random_index]
    percentage_change_in_price = round(
        product_chosen_for_insight["percentage_change_in_price"]
    )
    if product_chosen_for_insight["percentage_change_in_price"] > 0:
        insight = (
            f"Product {product_chosen_for_insight['product'].title} "
            f"has had a increase in price by {percentage_change_in_price}% "
            f"in the last {lookback_days} days."
        )
    elif product_chosen_for_insight["percentage_change_in_price"] < 0:
        insight = (
            f"Product {product_chosen_for_insight['product'].title} "
            f"has had a {abs(percentage_change_in_price)}% decrease "
            f"in price over the last {lookback_days} days."
        )
    else:
        insight = (
            f"Your search results didn't have price changes over the"
            f" last {lookback_days} days, act now before price changes."
        )

    price_change_insight = {
        "product": product_chosen_for_insight["product"],
        "insight": insight,
        "email": alert.email,
    }

    return price_change_insight


def generate_insights(lookback_days=14) -> list[dict]:
    """
    Generate insights for all alerts
    """
    # Get active alerts one
    active_alerts = ActiveAlert.objects.filter(is_active=True)

    insights: list[dict] = []
    for alert in active_alerts:
        # Fetch the tracked products for the alert
        tracked_products = alert.tracked_products.all()
        tracked_product_ids = [product.item_id for product in tracked_products]

        # Calculate the average price of each of the tracked products
        # over the lookback days
        end_date = datetime.datetime.now(tz=datetime.UTC)
        start_date = end_date - datetime.timedelta(days=lookback_days)
        average_price_of_tracked_products: QuerySet[ProductPriceLog] = (
            ProductPriceLog.objects.filter(
                item_id__in=tracked_product_ids, timestamp__gte=start_date
            )
            .values("item_id")
            .annotate(average_price=Avg("price"))
        )

        average_price_by_product_id: dict[str : decimal.Decimal] = {
            product["item_id"]: product["average_price"]
            for product in average_price_of_tracked_products
        }
        price_change_insight: dict = gather_price_change_insight(
            tracked_products, average_price_by_product_id, lookback_days, alert
        )
        insights.append(price_change_insight)

    return insights
