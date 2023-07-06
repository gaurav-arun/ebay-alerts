API_CLIENT_CACHE_KEY_MAP = {
    'find_items_by_keyword': 'ebay_find_items_by_keyword'
}

# The token expires in 7200 seconds,
# but we want to cache it for a little less than that
REDUCE_EXPIRATION_TIME_BY = 60
