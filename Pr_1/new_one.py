import pandas as pd
import os

# os.chdir('C:/Users/User/.atom/ITMO_Work/4_Semestr/MEVD/Pr_1')

# take_table_sale = pd.read_csv('./sales_train.csv')
# take_table_shops = pd.read_csv('./shops.csv')
# take_table_categories = pd.read_csv('./item_categories.csv')
# take_table_items = pd.read_csv('./items.csv')

from google.colab import drive
drive.mount('/content/drive')

take_table_shops = pd.read_csv('/content/drive/MyDrive/data/shops.csv')
take_table_sale = pd.read_csv('/content/drive/MyDrive/data/sales_train.csv')
take_table_items = pd.read_csv('/content/drive/MyDrive/data/items.csv')
take_table_categories = pd.read_csv('/content/drive/MyDrive/data/item_categories.csv')


# 1.1 Задание
random_sales = take_table_sale.sample(n=10000, random_state=42) # n - количество случайных строк, random_state - для воспроизводимости. Глобальное случайное состояние
category_37 = take_table_items[take_table_items['category_id'] == 37]['item_id'].tolist()
fraction = random_sales[random_sales['item_id'].isin(category_37)].shape[0] / 10000 # .shape[0] размер по горизонтали - то есть количество строк

print('Задание 1')
print(f"1.1/ Доля товаров из категории 37: {fraction*100}%")

# 1.2 Задание
take_name_SPbCenter = take_table_shops.loc[take_table_shops['shop_name'] == ' St. Petersburg Nevsky Center shopping center'].iloc[0]['shop_id']

take_table_sale['date'] = pd.to_datetime(take_table_sale['date'], format='%d.%m.%Y')
table_2014 = take_table_sale[(take_table_sale['date'].between('2014-01-01', '2014-12-31')) & (take_table_sale['shop_id'] == take_name_SPbCenter)]

sales_by_date = table_2014.groupby('date')['item_cnt_day'].sum().reset_index()
best_day = sales_by_date.loc[sales_by_date['item_cnt_day'].idxmax()]
print()
print('1.2/ Самый удачный день для магазина St. Petersburg Nevsky Center shopping center в 2014 году:',
      best_day['date'], '\n     Количество продаж в этот день:', best_day['item_cnt_day'])

# 1.3 Задание
sales_items = take_table_sale.merge(take_table_items, on='item_id')
# группируем данные по месяцам и id товара. Группируем продажи по месяцам и товарам и считаем суммарные продажи каждого товара за каждый месяц.
sales_by_month_item = sales_items.groupby(['date_block_num', 'item_id']).sum()

# выбираем товар с максимальным количеством продаж для каждого месяца
best_selling_items = sales_by_month_item.groupby('date_block_num').idxmax()['item_cnt_day']
# print(sales_by_month_item)
print()
print('1.3/ Лучший товар по количеству продаж в магазинах за каждый месяц:')
for i in range(1, 34):  # месяца date_block_num
    # id товара с максимальным количеством продаж
    item_id = best_selling_items[i][1]
    item_name = take_table_items.loc[take_table_items['item_id'] == item_id]['item_name'].values[0] # имя товара
    print(f"     За {i} месяц: {item_name}")

# print(take_table_sale.groupby('date')['date_block_num'].max())

# 2.1 Задание

top_items = sales_by_month_item.groupby('item_id')['item_cnt_day'].sum().sort_values(ascending=False).head(10)
top_items_name = take_table_items.loc[take_table_items['item_id'].isin(top_items.index.to_list())]['item_name'].tolist()
# print(top_items)
print('2.1/ Топ-10 товаров по количеству продаж')
for i in range(10):
    print(f"     {i+1} товар по количеству продаж: {top_items_name[i]}")

# 2.2 Задание
all_tug_filt = top_items.index.to_list() 
years = [2013, 2014, 2015]
item_sets = []
# выделим год из даты, используя метод .apply() и лямбда-функцию, которая будет применяться к каждому элементу столбца 'date' и возвращать год
for year in years:
    item_sets.append(set(take_table_sale[take_table_sale['date'].apply(lambda x: x.year) == year]['item_id']))

# Все товары, которые продавались во всех трех годах
result = list(set.intersection(*item_sets))

all_year = set(all_tug_filt).intersection(result)
print()
if (all_year):
    for i in all_year:
        name = take_table_items.loc[take_table_items['item_id'] == i]["item_name"].iloc[0]
        print(f'     Из них продавались все три года: {name}')
else:
    print('     Тех, что продавались все три года не существует')

# 3.1 Задание
id_num_unique = take_table_sale['item_id'].value_counts().index.to_list()
val_of_id = take_table_sale['item_id'].value_counts().tolist()

count_of_cats = [0]*len(take_table_categories)

for i in range(len(id_num_unique)):
    cat = take_table_items[take_table_items.item_id == id_num_unique[i]].values.tolist()[0][2]
    count_of_cats[cat] += val_of_id[i]

take_table_categories['sales'] = count_of_cats
min_category_id_1 = take_table_categories.loc[take_table_categories['sales'] == take_table_categories['sales'].min()]['item_category_id'].values.tolist()[0]
min_category_id_2 = take_table_categories.loc[take_table_categories['sales'] == take_table_categories['sales'].min()]['item_category_id'].values.tolist()[1]
print(f"3.1/ Категории товаров с минимальным количеством продаж: {min_category_id_1}, {min_category_id_2}")

# 3.2 Задание
max_category_id = take_table_categories.loc[take_table_categories['sales'] == take_table_categories['sales'].max()]['item_category_id'].values.tolist()[0]

print(f"3.2/ Категория товаров с максимальным количеством продаж: {max_category_id}")

# 4.1 Задание 
cats = [min_category_id_1, min_category_id_2, max_category_id]

take_table_categories.rename(columns={'item_category_id': 'category_id'}, inplace=True)

table_merdge = pd.merge(take_table_sale, take_table_items, on='item_id')
table_merdge = pd.merge(table_merdge, take_table_categories, on='category_id')
table_merdge_last = pd.merge(table_merdge, take_table_shops, on='shop_id')

# Вычислим общее количество продаж каждого товара в 5 магазинах с наибольшими продажами
top_5_shops = table_merdge_last.groupby('shop_id')['item_cnt_day'].sum().nlargest(5).index.to_list()
table_merdge_last = table_merdge_last.loc[(table_merdge_last['shop_id'].isin(top_5_shops)) & (table_merdge_last['category_id'].isin(cats))]

sales_by_item = table_merdge_last.groupby(['shop_id', 'item_id'])['item_cnt_day'].sum().reset_index()
sales_by_item = sales_by_item.groupby(['shop_id', 'item_id'])['item_cnt_day'].mean().reset_index()

sales_filtered = sales_by_item[sales_by_item['item_cnt_day'] > 100]
print()
print('4.1/ Товары, среднее количество продаж которых строго больше 100 в 5 магазинах с наибольшими продажами:')
print(sales_filtered)





# 4.2 Задание


unique_id_item = sales_filtered['item_id'].unique()
max_sales = take_table_sale.groupby(['item_id', 'date_block_num'])['item_cnt_day'].max()


# max_sales = max_sales.loc[max_sales.index.get_level_values('item_id').isin(unique_id_item)]
# max_month = max_sales.groupby('item_id').idxmax().to_frame().reset_index()

max_sales = take_table_sale.groupby(['item_id', 'date_block_num']).agg({'item_cnt_day': 'max', 'date': 'first'})
max_sales = max_sales.loc[max_sales.index.get_level_values('item_id').isin(unique_id_item)]
max_month = max_sales.groupby('item_id').apply(lambda x: x.loc[x['item_cnt_day'].idxmax()])


# номер месяца с максимальным значением item_cnt_day
print("4.2/ Месяц с максимальными продажами для каждого товара:")
print(max_month)

# 5.1.1 Задание

category_sales_max = take_table_sale[take_table_sale['item_id'].isin(take_table_items[take_table_items['category_id'] == max_category_id]['item_id'])]
# для каждой группы, для столбца item_price вычисляются среднее и медианное значение при помощи метода agg() и передачи словаря с указаниями
sales_by_month_category = category_sales_max.groupby(['date_block_num', 'item_id']).agg({'item_price': ['mean', 'median']})

# Сортировка таблицы по убыванию средней цены
top_10_categories = sales_by_month_category.groupby('item_id').mean().sort_values(('item_price', 'mean'), ascending=False).head(10)
res = take_table_items.loc[take_table_items['item_id'].isin(top_10_categories.index.tolist())]['item_name'].tolist()
mn = top_10_categories['item_price']['mean'].tolist()
md = top_10_categories['item_price']['median'].tolist()
# print('------------------------')
# print(top_10_categories)
print()
print(
    f"5.1.1 max_id=40/ Топ-10 товаров по средней цене в категории с максимальным количеством продаж:")
for i in range(len(res)):
    print(
        f"     {i + 1}. {res[i]}; Средняя цена: {mn[i]}; Медианная цена: {md[i]}")

# 5.1.2 Задание

category_sales_max = take_table_sale[take_table_sale['item_id'].isin(take_table_items[take_table_items['category_id'] == min_category_id_1]['item_id'])]
# для каждой группы, для столбца item_price вычисляются среднее и медианное значение при помощи метода agg() и передачи словаря с указаниями
sales_by_month_category = category_sales_max.groupby(['date_block_num', 'item_id']).agg({'item_price': ['mean', 'median']})

# Сортировка таблицы по убыванию средней цены
top_10_categories = sales_by_month_category.groupby('item_id').mean().sort_values(('item_price', 'mean'), ascending=False).head(10)
res = take_table_items.loc[take_table_items['item_id'].isin(top_10_categories.index.tolist())]['item_name'].tolist()
mn = top_10_categories['item_price']['mean'].tolist()
md = top_10_categories['item_price']['median'].tolist()
# print('------------------------')
# print(top_10_categories)
print()
print(
    f"5.1.1 min_1_id=10/ Топ-10 товаров по средней цене в категории с максимальным количеством продаж:")
for i in range(len(res)):
    print(
        f"     {i + 1}. {res[i]}; Средняя цена: {mn[i]}; Медианная цена: {md[i]}")
    
# 5.1.3 Задание

category_sales_min = take_table_sale[take_table_sale['item_id'].isin(take_table_items[take_table_items['category_id'] == min_category_id_2]['item_id'])]
sales_by_month_category_min = category_sales_min.groupby(['date_block_num', 'item_id']).agg({'item_price': ['mean', 'median']})

# Сортировка таблицы по убыванию средней цены
top_10_categories_min = sales_by_month_category_min.groupby('item_id').mean().sort_values(('item_price', 'mean'), ascending=False).head(10)
res_min = take_table_items.loc[take_table_items['item_id'].isin(top_10_categories_min.index.tolist())]['item_name'].tolist()
mn_mn = top_10_categories_min['item_price']['mean'].tolist()
md_mn = top_10_categories_min['item_price']['median'].tolist()
print()
print(
    f"5.1.1 min_id_2=51/ Топ-10 товаров по средней цене в категории с минимальным количеством продаж:")
for i in range(len(res_min)):
    print(
        f"     {i + 1}. {res_min[i]}; Средняя цена: {mn_mn[i]}; Медианная цена: {md_mn[i]}")

# 5.2 Задание

take_table_sale['year'] = take_table_sale['date'].dt.year
mean_prices = take_table_sale.groupby(['year', take_table_sale['date'].dt.month])['item_price'].mean()

previous_month = mean_prices.shift(1, fill_value=0)
next_month = mean_prices.shift(-1, fill_value=0)

result_5_2 = mean_prices[(mean_prices < previous_month) & (mean_prices < next_month)]
res_year = set(result_5_2.index.get_level_values(0).tolist())
res_date = result_5_2.index.get_level_values(1).tolist()
print()
print('5.2/ Месяцы, в которых средняя цена меньше, чем в предыдущем и следующем месяце:')
print(result_5_2)

(min_sales)


