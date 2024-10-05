import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets (Pastikan file sudah ada di path yang benar)
customers_df = pd.read_csv("customers_dataset.csv")
order_items_df = pd.read_csv("order_items_dataset.csv")
orders_df = pd.read_csv("orders_dataset.csv")
products_df = pd.read_csv("products_dataset.csv")
sellers_df = pd.read_csv("sellers_dataset.csv")

# Pastikan 'order_purchase_timestamp' adalah datetime
orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])

# Sidebar untuk memilih jumlah bulan terakhir
st.sidebar.header("Filter Options")
months = st.sidebar.slider("Pilih rentan bulan", 1, 6, 6)  # Default to 6 months

# Filter orders data untuk beberapa bulan terakhir
last_order_date = orders_df['order_purchase_timestamp'].max()
filter_date = last_order_date - pd.DateOffset(months=months)
recent_orders_df = orders_df[orders_df['order_purchase_timestamp'] >= filter_date]

# Gabungkan orders_df dan customers_df
merged_orders_customers_df = pd.merge(recent_orders_df, customers_df, on='customer_id', how='inner')

# 1. **Frekuensi Pembelian Pelanggan**
st.header(f"Frekuensi Pembelian Pelanggan dalam {months} Bulan Terakhir di Toko Salaisha Ghina")

# Hitung frekuensi pembelian per pelanggan
purchase_frequency = merged_orders_customers_df.groupby('customer_unique_id').size().reset_index(name='purchase_count')

# Tampilkan jumlah total pelanggan unik
st.write(f"Adapun total pelanggan dalam {months} bulan terakhir:", len(purchase_frequency))

# Visualisasi frekuensi pembelian
st.subheader("Distribusi Frekuensi Pembelian Pelanggan")
plt.figure(figsize=(10, 6))
sns.histplot(purchase_frequency['purchase_count'], bins=10, color='skyblue')
plt.title('Frekuensi Pembelian dalam Beberapa Bulan Terakhir')
plt.xlabel('Jumlah Pembelian')
plt.ylabel('Jumlah Pelanggan')
st.pyplot(plt)

# 2. **Produk dengan Pendapatan Tertinggi**
st.header("Top 10 Produk Berdasarkan Pendapatan")

# Gabungkan order_items_df dan products_df
merged_order_items_products = pd.merge(order_items_df, products_df, on='product_id')

# Hitung total pendapatan untuk setiap produk
sales_by_product = merged_order_items_products.groupby('product_category_name').agg({'price': 'sum'}).reset_index()
sales_by_product.columns = ['product_category_name', 'total_revenue']

# Pilih 10 produk teratas berdasarkan pendapatan
top_revenue_products = sales_by_product.sort_values(by='total_revenue', ascending=False).head(10)

# Tampilkan data produk teratas
st.write(top_revenue_products)

# Visualisasi produk dengan pendapatan tertinggi
st.subheader("Top 10 Produk dengan Pendapatan Tertinggi")
plt.figure(figsize=(10, 6))
sns.barplot(x='total_revenue', y='product_category_name', data=top_revenue_products, palette='viridis')
plt.title('Top 10 Produk dengan Pendapatan Tertinggi')
plt.xlabel('Total Revenue')
plt.ylabel('Product Category Name')
st.pyplot(plt)

# 3. **Produk dengan Kuantitas Penjualan Tertinggi**
st.header("Top 10 Produk Berdasarkan Kuantitas Penjualan")

# Hitung total kuantitas penjualan untuk setiap produk
sales_quantity_by_product = merged_order_items_products.groupby('product_category_name').agg({'order_item_id': 'count'}).reset_index()
sales_quantity_by_product.columns = ['product_category_name', 'total_sales_quantity']

# Pilih 10 produk teratas berdasarkan kuantitas penjualan
top_sales_products = sales_quantity_by_product.sort_values(by='total_sales_quantity', ascending=False).head(10)

# Tampilkan data produk teratas berdasarkan kuantitas penjualan
st.write(top_sales_products)

# Visualisasi produk dengan kuantitas penjualan tertinggi
st.subheader("Top 10 Produk dengan Kuantitas Penjualan Tertinggi")
plt.figure(figsize=(10, 6))
sns.barplot(x='total_sales_quantity', y='product_category_name', data=top_sales_products, palette='Blues')
plt.title('Top 10 Produk dengan Kuantitas Penjualan Tertinggi')
plt.xlabel('Total Sales Quantity')
plt.ylabel('Product Category Name')
st.pyplot(plt)

# Sidebar informasi
st.sidebar.text("Dashboard dibuat oleh m319b4kx4016@bangkit.academy")
