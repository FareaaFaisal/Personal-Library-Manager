import streamlit as st
import json
import os

# Define file to store books
BOOKS_FILE = "books_data.json"

# Load books from file
def load_books():
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r") as file:
            return json.load(file)
    return []

# Save books to file
def save_books(books):
    with open(BOOKS_FILE, "w") as file:
        json.dump(books, file, indent=4)

# UI 
st.markdown(
    """
    <style>
        .main {background-color: #FAD0C4;}
        .stSidebar {background-color: #007074;}
        .stButton>button {background-color: #007074; color: white;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation
st.sidebar.markdown("# 📚 Personal Library Manager")

menu = st.sidebar.radio("Select an option:", [
    "Add New Book", "View Books", "Search Book", "Update Book", "Delete Book", "Display Statistics"
])

books = load_books()

if menu == "Add New Book":
    st.title("📖 Add a New Book")
    title = st.text_input("📕 Book Title")
    author = st.text_input("✍️ Author")
    year = st.text_input("📅 Publication Year")
    genre = st.text_input("📚 Genre")
    read = st.checkbox("✔ Have you read this book?")
    if st.button("➕ Add Book"):
        books.append({"title": title, "author": author, "year": year, "genre": genre, "read": read})
        save_books(books)
        st.success("🎉 Book added successfully!")

elif menu == "View Books":
    st.title("📚 Your Book Collection")
    if books:
        for book in books:
            st.write(f"**📖 {book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✔ Read' if book['read'] else '❌ Unread'}")
    else:
        st.info("ℹ️ No books added yet.")

elif menu == "Search Book":
    st.title("🔍 Search for a Book")
    query = st.text_input(" Enter Book Title or Author")
    if st.button("🔍 Search"):
        results = [book for book in books if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]
        if results:
            for book in results:
                st.write(f"**📖 {book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✔ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("⚠️ No books found.")

elif menu == "Update Book":
    st.title("✏ Update Book Details")
    book_titles = [book['title'] for book in books]
    selected_book = st.selectbox("📌 Select a book to update", book_titles)
    if selected_book:
        book = next(b for b in books if b['title'] == selected_book)
        book['title'] = st.text_input("📖 Book Title", value=book['title'])
        book['author'] = st.text_input("✍️ Author", value=book['author'])
        book['year'] = st.text_input("📅 Publication Year", value=book['year'])
        book['genre'] = st.text_input("📚 Genre", value=book['genre'])
        book['read'] = st.checkbox("✔ Have you read this book?", value=book['read'])
        if st.button("✅ Update Book"):
            save_books(books)
            st.success("✔ Book updated successfully!")

elif menu == "Delete Book":
    st.title("🗑 Delete a Book")
    book_titles = [book['title'] for book in books]
    selected_book = st.selectbox("❌ Select a book to delete", book_titles)
    if st.button("🗑 Delete Book"):
        books = [book for book in books if book['title'] != selected_book]
        save_books(books)
        st.success("🗑 Book deleted successfully!")

elif menu == "Display Statistics":
    st.title("📊 Library Statistics")

    total_books = len(books)
    read_books = sum(1 for book in books if book['read'])
    unread_books = total_books - read_books
    read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0  # Avoid division by zero

    # Display key statistics
    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"✅ **Books Read:** {read_books} ({read_percentage:.2f}%)")
    st.write(f"📕 **Books Unread:** {unread_books}")

    if total_books > 0:
        # Data for Streamlit bar chart
        progress_data = {"Category": ["Read 📖", "Unread 📕"], "Count": [read_books, unread_books]}

        # Display the bar chart
        st.bar_chart(progress_data, x="Category", y="Count", use_container_width=True)
    else:
        st.info("ℹ️ No books added yet.")
