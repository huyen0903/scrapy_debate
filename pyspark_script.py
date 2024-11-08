from pyspark.sql import SparkSession, DataFrame, Row
from pyspark.sql.functions import row_number, col, when, split, regexp_replace, regexp_extract, format_number, udf
import psycopg2
import logging
import findspark
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sqlalchemy import create_engine
from pyspark.sql.functions import concat_ws
from pyspark.sql.functions import udf, hash, explode
from pyspark.sql.functions import monotonically_increasing_id, concat, lit
from pyspark.sql.types import StructType, StructField,ArrayType, StringType, IntegerType, DateType
from pyspark.sql.window import Window
from pyspark.ml.feature import NGram, Tokenizer, StopWordsRemover
# Initialize Spark session with MongoDB and PostgreSQL connectors
from pyspark.sql.functions import to_timestamp, col, trim, date_format, to_date
from pyspark.sql import functions as F
from pyspark.sql import types as T
# from googletrans import Translator
from deep_translator import GoogleTranslator
# Initialize Translator

# Define a function to translate text
# def translate_text(text):
#     try:
#         translator = Translator()
#         return translator.translate(text, src='auto', dest='vi').text
#     except Exception as e:
#         return str(e)
    

# translate_udf = udf(lambda x: translate_text(x), StringType())
# Hàm dịch sử dụng googletrans
def translate_text(text, target_lang="vi"):
    # translator = Translator()ư
    if text:
        try:
                # Chia đoạn văn bản thành các câu theo dấu chấm
            sentences = text.split('.')
            translated_sentences = []
            if (sentences):
                logging.error(f"done translate_text': {str(text)}")
            else:
                sentences.append(text)
            for sentence in sentences:
                    # Loại bỏ khoảng trắng thừa
                    sentence = sentence.strip()
                    if sentence:  # Kiểm tra câu không rỗng
                        try:
                            translated = GoogleTranslator(source='auto', target=target_lang).translate(sentence)
                            translated_sentences.append(translated)
                        except Exception as e:
                            logging.error(f"Error during translation of '{sentence}': {str(e)}")
                            # Nếu có lỗi, thêm câu gốc vào danh sách kết quả
                            # translated_sentences.append(sentence)
                            

                # Ghép lại các câu đã dịch
            return '. '.join(translated_sentences)
        except Exception as e:
            logging.error(f"Error during: {str(e)}")
            logging.error(f"Error during text: {str(text)}")
            return text  # Trường hợp gặp lỗi, trả về nội dung ban đầu
    else:
        return ""
    
def translate_text_array(arr_text, target_lang="vi"):
    # translator = Translator()ư
    if arr_text:
        try:
            result= []
            for text in arr_text:
                sentences = text.split('.')
                translated_sentences = []
                if (sentences):
                    logging.error(f"done translate_text_array': {str(text)}")
                else:
                    sentences.append(text)
                for sentence in sentences:
                        # Loại bỏ khoảng trắng thừa
                        sentence = sentence.strip()
                        if sentence:  # Kiểm tra câu không rỗng
                            try:
                                translated = GoogleTranslator(source='auto', target=target_lang).translate(sentence)
                                translated_sentences.append(translated)
                            except Exception as e:
                                logging.error(f"Error during translation of '{sentence}': {str(e)}")
                                # Nếu có lỗi, thêm câu gốc vào danh sách kết quả
                                # translated_sentences.append(sentence)
                                

                    # Ghép lại các câu đã dịch
                result.append('. '.join(translated_sentences))
            return result
        except Exception as e:
            logging.error(f"Error during: {str(e)}")
            logging.error(f"Error during text: {str(text)}")
            return text  # Trường hợp gặp lỗi, trả về nội dung ban đầu
    else:
        return ""

# Tạo UDF để áp dụng hàm dịch vào cột dữ liệu
translate_udf = udf(lambda x: translate_text(x), StringType())
translate_udf_array = udf(translate_text_array, ArrayType(StringType()))
# translate_udf = udf(translate_text, StringType())
spark = SparkSession.builder \
.appName("Chuyển đổi MongoDB sang PostgreSQL") \
.config("spark.mongodb.input.uri", "mongodb://mongodb:27017/debate_db") \
.config("spark.mongodb.input.collection", "debate") \
.config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,org.postgresql:postgresql:42.2.24") \
.config("spark.executor.memory", "8g") \
.config("spark.driver.memory", "8g") \
.config("spark.task.maxFailures", "8") \
.config("spark.python.worker.reuse", "true") \
.getOrCreate()

logging.debug("Phiên Spark đã được khởi tạo.")

# Load data from MongoDB
df = spark.read.format("mongo").option("forceDeleteTempCheckpointLocation", "true").load()
so_luong_tai_lieu = df.count()
df.printSchema()
logging.debug("DataFrame đã được tạo từ MongoDB.")

# Select specific columns
df = df.select(
    "motion", "points_for", "points_against", "bibliography", 
    "post_type", "post_date", "describe","topic_name",
)

# Create 'Street' column based on the 'Address' column if 'Street' is null
# df = df.withColumn(
#     "Street",
#     when(
#         col("Street").isNull(),
#         split(col("Address"), ",")[0]  # Lấy chuỗi ký tự trước dấu ','
#     ).otherwise(col("Street"))
# )

# Lọc và giữ lại các dòng có giá trị không phải là null
# df = df.filter(col("District").isNotNull())
# df = df.filter(col("Ward").isNotNull())
# df = df.filter(col("Poster").isNotNull())

# Loại bỏ từ "Đường" khỏi cột 'Street'
# df = df.withColumn("Street", regexp_replace(col("Street"), "Đường", ""))
# df = df.withColumn("Ward", regexp_replace(col("Ward"), "Phường", ""))
# df = df.withColumn("Ward", regexp_replace(col("Ward"), "Xã", ""))
# df = df.withColumn("District", regexp_replace(col("District"), "Quận", ""))
# df = df.withColumn("District", regexp_replace(col("District"), "Huyện", ""))

# Trích xuất chỉ số từ cột 'Bedrooms'
# df = df.withColumn("Bedrooms", regexp_extract(col("Bedrooms"), r'\d+', 0).cast("int"))

# Xử lý cột 'Room_area': Trích xuất dữ liệu số và đổi tên thành 'Room_area_m2'
# df = df.withColumn(
#     "Room_area_m2",
#     regexp_extract(col("Room_area"), r'(\d+)', 1).cast("int")
# )

# Xử lý cột 'Rental_price': Trích xuất dữ liệu số và thay thế ' Triệu'
# df = df.withColumn(
#     "Price_per_month",
#     regexp_extract(col("Rental_price"), r'(\d+)', 1).cast("int") * 1000000
# )

# Xóa cột 'Rental_price'
# df = df.drop("Rental_price")

# Xóa cột 'Room_area' nếu bạn không cần nó nữa
# df = df.drop("Room_area")

# Trích xuất số từ cột 'Toilets' và chuyển đổi thành kiểu số nguyên
# df = df.withColumn(
#     "Toilets",
#     regexp_extract(col("Toilets"), r'\d+', 0).cast("int")
# )

# Chuyển DataFrame PySpark sang DataFrame Pandas
pandas_df = df.toPandas()

# Điền giá trị thiếu bằng dữ liệu trước đó trong Pandas DataFrame
# pandas_df['Toilets'] = pandas_df['Toilets'].fillna(method='ffill')
# pandas_df['Bedrooms'] = pandas_df['Bedrooms'].fillna(method='ffill')

# Chuyển DataFrame Pandas quay lại PySpark DataFrame
df = spark.createDataFrame(pandas_df)

# Định nghĩa hàm để viết hoa chữ cái đầu tiên của mỗi từ
def capitalize_first_letter(text):
    return ' '.join(word.capitalize() for word in text.split()) if text else text

# Đăng ký hàm như một UDF
capitalize_udf = udf(capitalize_first_letter, StringType())

# Áp dụng hàm UDF lên cột 'Street'
# df = df.withColumn("Street", capitalize_udf(col("Street")))

# Chọn các cột cụ thể sau khi đã xử lý
df = df.select(
    # "posting_id", "title", "address", "street", "ward", "district", "city", "price_per_month",
    # "room_area_m2", "bedrooms", "toilets", "poster", "posting_date", "type_of_listing", "view",
    # "describe"
    "topic_name", "motion", "points_for", "points_against", "bibliography", 
    "post_type", "post_date", "describe",
)
df = df.withColumnRenamed('topic_name', 'topic_name')
df = df.withColumnRenamed('motion', 'motion')
df = df.withColumnRenamed('points_for', 'points_for')
df = df.withColumnRenamed('points_against', 'points_against')
df = df.withColumnRenamed('bibliography', 'bibliography')
df = df.withColumnRenamed('post_type', 'post_type')
df = df.withColumnRenamed('post_date', 'post_date')
df = df.withColumnRenamed('describe', 'describe')
# df = df.withColumnRenamed('type_of_listing', 'type_listing')

    # 1. Chọn các cột cần thiết và loại bỏ các giá trị trùng lặp
house_df = df.select(
    col("motion").alias("motion"),
    col("topic_name").alias("topic_name"),
    col("points_for").alias("points_for"),
    col("points_against").alias("points_against"),
    col("bibliography").alias("bibliography"),
    col("post_type").alias("post_type"),
    col("post_date").alias("post_date"),
    col("describe").alias("describe"),
    # col("num_bedrooms").cast("int").alias("num_bedrooms"),
    # col("num_toilets").cast("int").alias("num_toilets"),
    # col("room_area").cast("int").alias("room_area"),
    # col("city").alias("city"),
    # col("district").alias("district"),
    # col("ward").alias("ward"),
    # col("street").alias("street")
).distinct()  # Loại bỏ các giá trị trùng lặp
    # Tạo cột index từ 0 trở đi
# translate_udf = udf(translate_text_google, StringType())
# translate_udf = udf(lambda text: translate_text_google(text), StringType())
# translate_udf = udf(translate_text_google, StringType())
house_df = house_df.withColumn("index", monotonically_increasing_id())
# house_df_vi = house_df.withColumn("motion_vi", 
#                                translate_udf(house_df["motion"])
#      )
# house_df_vi = house_df.withColumn("topic_name_vi", translate_udf(house_df["topic_name"]))  # Replace 'text_column'
# house_df_vi = house_df.withColumn("post_type_vi", translate_udf(house_df["post_type"]))  # Replace 'text_column'
# house_df_vi = house_df.withColumn("describe_vi", translate_udf(house_df["describe"]))  # Replace 'text_column'
# house_df_vi = house_df.select("topic_name","post_type","describe","index").toPandas()
# house_df_vi = house_df_vi.withColumn("motion_vi", translate_udf(house_df_vi["motion"]))  

logging.debug("house_df_vi")

house_df = house_df.withColumn("formatted_date", date_format(to_date(trim(regexp_replace("post_date", r"[\s\n]+", " ")), "MMM dd, yyyy"), "dd-MM-yyyy"))

house_df = house_df.withColumn("motion", trim(house_df["motion"]))
house_df = house_df.withColumn("topic_name", trim(house_df["topic_name"]))
house_df = house_df.withColumn("post_type", trim(house_df["post_type"]))
house_df = house_df.withColumn("post_date", trim(house_df["post_date"]))
house_df = house_df.withColumn("describe", trim(house_df["describe"]))
house_df_vi = house_df.select(
    col("motion").alias("motion"),
    col("topic_name").alias("topic_name"),
    col("points_for").alias("points_for"),
    col("points_against").alias("points_against"),
    col("bibliography").alias("bibliography"),
    col("post_type").alias("post_type"),
    col("post_date").alias("post_date"),
    col("describe").alias("describe"),
    col("index").alias("house_index"),
).distinct()  # Loại bỏ các giá trị trùng lặp
house_df_vi = house_df_vi.withColumn("motion", translate_udf(house_df_vi["motion"]))  
# house_df_vi = house_df_vi.withColumn("post_type_vi", translate_udf(house_df_vi["post_type"]))  
house_df_vi = house_df_vi.withColumn("post_type", translate_udf(house_df_vi["post_type"]))  
house_df_vi = house_df_vi.withColumn("describe", translate_udf(house_df_vi["describe"]))  
house_df_vi = house_df_vi.withColumn("topic_name", translate_udf(house_df_vi["topic_name"]))  
house_df_vi = house_df_vi.withColumn("points_for", translate_udf_array(house_df_vi["points_for"]))  
house_df_vi = house_df_vi.withColumn("points_against", translate_udf_array(house_df_vi["points_against"]))  
house_df_vi = house_df_vi.select(
    col("motion").alias("motion"),
    col("topic_name").alias("topic_name"),
    col("points_for").alias("points_for"),
    col("points_against").alias("points_against"),
    col("bibliography").alias("bibliography"),
    col("post_type").alias("post_type"),
    col("post_date").alias("post_date"),
    col("describe").alias("describe"),
    col("house_index").alias("house_index"),
).distinct()  # Loại bỏ các giá trị trùng lặp
# house_df_vi = house_df_vi.withColumn("index", monotonically_increasing_id())
# Tạo cột house_id với định dạng 'WE' và bắt đầu từ 100
# house_df_with_id = house_df.withColumn(
#     "motion_id",
#     concat(lit("P"), (col("index") + 100).cast("string"))
# ).drop("index")  # Bỏ cột index nếu không còn cần thiết
# house_df_vi = house_df_vi.drop("motion")
# house_df_vi = house_df_vi.drop("topic_name")
# house_df_vi = house_df_vi.drop("post_date")
# house_df_vi = house_df_vi.drop("post_type")
# house_df_vi = house_df_vi.drop("describe")
join_columns = ["motion",  "topic_name", "motion", "points_for", "points_against", "bibliography", 
    "post_type", "post_date", "describe"
    # , "formatted_date","formatted_type"
                # , "num_bedrooms", "num_toilets", "room_area", "city", "district", "ward", "street"
                ]
# Thực hiện join
# df = df.join(
#     house_df_with_id,
#     on=join_columns,
#     how="left")

# post_df = df.select(
#     col("post_id").alias("post_id"),  # Không thay đổi
#     col("views").cast("int").alias("views"),  # Chuyển đổi từ string sang int
#     col("type_listing").alias("type_listing"),  # Không thay đổi
#     col("rental_price").cast("int").alias("rental_price"),  # Chuyển đổi từ string sang float
#     col("title").alias("title"),  # Không thay đổi
#     col("poster").alias("poster"),  # Không thay đổi
#     col("content").alias("content"),
#     col("house_id").alias("house_id")  # Không thay đổi
# )    


# NGHIÊN CỨU
# amenity_schema = StructType([
#     StructField("amenity_id", StringType(), False),
#     StructField("amenity_name", StringType(), False),
#     StructField("amenity_category", StringType(), False)
# ])

# amenity_df = spark.createDataFrame([], amenity_schema)

# Dictionary amenities
# amenities = {
#     'Interior': ['nội thất', 'nhà bếp', 'tủ'],
#     'Exterior': ['ban công', 'cửa sổ', 'có sân'],
#     'Facilities': ['wifi', 'thang máy', 'máy lạnh'],
#     'Location': ['mặt tiền', 'hẻm', 'gần'],
#     'Pricing': ['thương lượng', 'ưu tiên', 'hợp đồng']
# }
# Chuyển đổi dictionary thành list các Row
# data = []
# for category, names in amenities.items():
#     for name in names:
#         data.append(Row(amenity_name=name, amenity_category=category))

# Tạo DataFrame từ list các Row
# new_amenities_df = spark.createDataFrame(data)

# Tạo cột amenity_id với định dạng 'AM' và bắt đầu từ 1000
# windowSpec = Window.orderBy("amenity_name")  # Sắp xếp theo amenity_name để đảm bảo thứ tự

# new_amenities_df_with_id = new_amenities_df.withColumn(
#     "amenity_id",
#     concat(lit("AM"), (row_number().over(windowSpec) + 999).cast("string"))
# )
# # Kết hợp dữ liệu từ new_amenities_df_with_id vào amenity_df
# amenity_df = amenity_df.union(new_amenities_df_with_id)

#================== xử lý NLP==============
# Step 1: Tokenize the content
# post_df = df.withColumn("content_str", concat_ws(" ", col("content")))

# Step 1: Tokenize the content
# tokenizer = Tokenizer(inputCol="content_str", outputCol="words")
# wordsData = tokenizer.transform(post_df)

# Custom list of Vietnamese stopwords
# vietnamese_stopwords = ["và", "của", "là", "có", "trong", "với", "cho", "các", "về", "tại", "những", "một", "cái", "đã", "đến", "đi"]

# Remove Stopwords using the custom list
# remover = StopWordsRemover(inputCol="words", outputCol="filtered_words", stopWords=vietnamese_stopwords)
# wordsData = remover.transform(wordsData)

# Step 2: Generate n-grams (unigram, bigram, trigram)
# ngram1 = NGram(n=1, inputCol="filtered_words", outputCol="unigrams")
# ngram2 = NGram(n=2, inputCol="filtered_words", outputCol="bigrams")
# ngram3 = NGram(n=3, inputCol="filtered_words", outputCol="trigrams")

# unigrams_df = ngram1.transform(wordsData)
# bigrams_df = ngram2.transform(wordsData)
# trigrams_df = ngram3.transform(wordsData)

# def extract_amenities(ngrams):
    
#     found_amenities = []
    
#     # Kiểm tra từng n-gram với các từ khóa từ dictionary
#     for ngram in ngrams:
#         for category, keywords in amenities.items():
#             for keyword in keywords:
#                 if keyword.lower() in ngram.lower():
#                     found_amenities.append(keyword)
                    
#     return list(set(found_amenities))  # Loại bỏ các giá trị trùng lặp

# Đăng ký hàm UDF
# extract_amenities_udf = udf(extract_amenities, ArrayType(StringType()))

# Áp dụng UDF lên cột 'trigrams' để trích xuất amenities
# amenities_df = trigrams_df.withColumn("extracted_amenities", extract_amenities_udf(col("trigrams")))

# Explode the amenities to create a row for each amenity
# post_amenity_temp_df = amenities_df.select(
#     col("post_id").alias("post_id"),
#     explode(col("extracted_amenities")).alias("amenity_name")
# ).dropna()



# Join with new_amenities_df_with_id to get amenity_id
# post_amenity_df = post_amenity_temp_df.join(
#     new_amenities_df_with_id,  # Joining with the DataFrame that contains amenity_id
#     on="amenity_name",         # Join on amenity_name column
#     how="left"                 # Perform a left join to include all rows from post_amenity_temp_df
# ).select(
#     col("post_id"),            # Select the post_id column from post_amenity_temp_df
#     col("amenity_id"),         # Select the amenity_id column from new_amenities_df_with_id
#     col("amenity_name")        # Select the amenity_name column from post_amenity_temp_df
# )

# Define the schema with nullable=False for post_id, amenity_id, and amenity_name
# post_amenity_schema = StructType([
#     StructField("post_id", StringType(), nullable=False),
#     StructField("amenity_id", StringType(), nullable=False),
#     StructField("amenity_name", StringType(), nullable=False)
# ])
# # Apply the schema when creating the DataFrame
# post_amenity_df_with_constraints = spark.createDataFrame(post_amenity_df.rdd, schema=post_amenity_schema)

# Ghi DataFrame vào PostgreSQL
# post_df.write \
#     .format("jdbc") \
#     .option("url", "jdbc:postgresql://postgres_db:5432/process_data") \
#     .option("dbtable", "post") \
#     .option("user", "root") \
#     .option("password", "root") \
#     .option("driver", "org.postgresql.Driver") \
#     .mode("overwrite") \
#     .save()

house_df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres_db:5432/process_data") \
    .option("dbtable", "house") \
    .option("user", "root") \
    .option("password", "root") \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite") \
    .save()
try:
    house_df_vi.show(truncate=False)
    logging.error(f"bbbbbbbbbbbbbbbbbbbbbbbbbbb")
    house_df_vi.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres_db:5432/process_data") \
        .option("dbtable", "house_vi") \
        .option("user", "root") \
        .option("password", "root") \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()
    house_df_vi.show(truncate=False)
    logging.error(f"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
except Exception as e:
    logging.error(f"Error during saving to PostgreSQL: {str(e)}")
# new_amenities_df_with_id.write \
#     .format("jdbc") \
#     .option("url", "jdbc:postgresql://postgres_db:5432/process_data") \
#     .option("dbtable", "amenity") \
#     .option("user", "root") \
#     .option("password", "root") \
#     .option("driver", "org.postgresql.Driver") \
#     .mode("overwrite") \
#     .save()

# post_amenity_df_with_constraints.write \
#     .format("jdbc") \
#     .option("url", "jdbc:postgresql://postgres_db:5432/process_data") \
#     .option("dbtable", "post_amenity") \
#     .option("user", "root") \
#     .option("password", "root") \
#     .option("driver", "org.postgresql.Driver") \
#     .mode("overwrite") \
#     .save()


