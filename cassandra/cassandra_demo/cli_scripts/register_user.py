from cassandra.cluster import Cluster

# اتصال به Cassandra
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('iut_ds')

# گرفتن ورودی از کاربر
print("🔹 ثبت‌نام کاربر جدید")
first_name = input("نام: ")
last_name = input("نام خانوادگی: ")
email = input("ایمیل: ")

# پیدا کردن بیشترین user_id فعلی برای اختصاص id جدید
rows = session.execute("SELECT MAX(user_id) AS max_id FROM users")
max_id = rows.one().max_id or 0
new_user_id = max_id + 1

# درج داده
session.execute("""
    INSERT INTO users (user_id, first_name, last_name, email)
    VALUES (%s, %s, %s, %s)
""", (new_user_id, first_name, last_name, email))

print(f"\n✅ کاربر با user_id={new_user_id} با موفقیت ثبت شد.")
cluster.shutdown()
