from .models import ActiveAlert, ProductPriceLog, ConsumedPubSubEvent
from django.db.models import Q, Max, Min, Avg, F
from datetime import datetime, timedelta


def gather_price_change_insight(product_ids, average_price_by_product_id, lookback_days=3) -> dict:
    """Gathers insights about the percentage price change from the
       average price of products over specified lookback days.
    """
    products = ProductPriceLog.objects.filter(item_id__in=product_ids)
    products_by_percentage_change_in_price = []
    for product in products:
        current_price = product.price
        average_price = average_price_by_product_id.get(product.item_id, 1)
        percentage_change_in_price_from_avg = ((current_price - average_price) / average_price) * 100
        products_by_percentage_change_in_price.append({
            'product': product,
            'percentage_change_in_price': percentage_change_in_price_from_avg
        })

    # sort products by percentage change in price
    products_by_percentage_change_in_price.sort(key=lambda x: x['percentage_change_in_price'], reverse=True)

    # Gather insight about the first product
    first_product = products_by_percentage_change_in_price[0]
    percentage_change_in_price = first_product['percentage_change_in_price']
    if first_product['percentage_change_in_price'] > 0:
        insight = f"Product {first_product['product'].title} has had a increase in price by {percentage_change_in_price}% " \
                  f"in the last {lookback_days} days."
    elif first_product['percentage_change_in_price'] < 0:
        insight = f"Product {first_product['product'].title} has had a {percentage_change_in_price}% decrease " \
                  f"in price over the last {lookback_days} days."
    else:
        insight = f"Your search results didn't have price changes over the last {lookback_days} days, " \
                  f"act now before price changes."

    price_change_insight = {
        'product': first_product['product'],
        'insight': insight
    }

    return price_change_insight


def generate_insights(lookback_days=3) -> list[dict]:
    """Generate insights for all alerts"""
    # TODO: Remove after testing
    active_alerts = ActiveAlert.objects.all().order_by('-id')[:1]

    insights: list[dict] = []
    for alert in active_alerts:
        product_ids = alert.tracked_products.all().values_list('item_id', flat=True)

        end_date = datetime.now().date()
        start_date = end_date - timedelta(weeks=2)

        # Perform the query, group by item_id, and calculate the average price for each product
        average_prices = ProductPriceLog.objects.filter(timestamp__range=(start_date, end_date)).values('item_id').annotate(average_price=Avg('price'))
        average_price_by_product_id = {average_price['item_id']: average_price['average_price'] for average_price in average_prices}

        price_change_insight = gather_price_change_insight(product_ids, average_price_by_product_id)
        price_change_insight['email'] = alert.email
        insights.append(price_change_insight)

    return insights
