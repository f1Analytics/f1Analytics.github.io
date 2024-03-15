from data_engine.main import GPBucket

bucket = GPBucket(2024, 2)
fig = bucket.get_quali_comparison(driver_1="VER", driver_2="LEC")

