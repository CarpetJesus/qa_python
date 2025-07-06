import pytest

from main import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

@pytest.fixture
def expected_genres():
    return ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']

@pytest.fixture
def age_rated_genres():
    return ['Ужасы', 'Детективы']


#Тесты для __init__

class TestBooksCollectorInit:

    def test_books_genre_empty(self, collector):
        assert collector.books_genre == {}

    def test_favorites_empty(self, collector):
        assert collector.favorites == []

    def test_genre_list_correct(self, collector, expected_genres):
        assert collector.genre == expected_genres

    def test_genre_age_rating_correct(self, collector, age_rated_genres):
        assert collector.genre_age_rating == age_rated_genres


# тесты для методов
class TestBooksCollectorMethods:

    # Тесты add.new_book
    @pytest.mark.parametrize("name, expected_result", [
        ("Темная Башня", 1),
        ("A", 1),
        ("A" * 39, 1),
        ("A" * 40, 1),
        ("", 0),
        ("A" * 41, 0)
    ])
    def test_add_new_book_with_valid_and_invalid_name(self, collector, name, expected_result):
        collector.add_new_book(name)
        assert len(collector.books_genre) == expected_result

    def test_add_new_book_duplicate(self, collector):
        collector.add_new_book("Темная Башня")
        collector.add_new_book("Темная Башня")
        assert len(collector.books_genre) == 1

    # Тесты set_book_genre
    def test_set_book_genre_valid(self, collector):
        collector.add_new_book("Темная Башня")
        collector.set_book_genre("Темная Башня", "Фантастика")
        assert collector.get_book_genre("Темная Башня") == "Фантастика"

    def test_set_book_genre_invalid_genre(self, collector):
        collector.add_new_book("Темная Башня")
        collector.set_book_genre("Темная Башня", "Мюзикл")
        assert collector.get_book_genre("Темная Башня") == ''

    def test_set_book_genre_invalid_book(self, collector):
        collector.set_book_genre("Неизвестная книга", "Фантастика")
        assert "Неизвестная книга" not in collector.books_genre

    # Тесты get_books_with_specific_genre
    def test_get_books_with_specific_genre_with_valid_name_and_genre(self, collector):
        collector.add_new_book("Темная Башня")
        collector.add_new_book("Властелин Колец")
        collector.set_book_genre("Темная Башня", "Фантастика")
        collector.set_book_genre("Властелин Колец", "Фантастика")
        assert collector.get_books_with_specific_genre("Фантастика") == ["Темная Башня", "Властелин Колец"]

    def test_get_books_with_specific_genre_empty(self, collector):
        assert collector.get_books_with_specific_genre("Фантастика") == []

    # Тесты get_books_genre
    def test_get_books_genre_with_valid_name_and_genre(self, collector):
        collector.add_new_book("Темная Башня")
        collector.set_book_genre("Темная Башня", "Фантастика")
        assert collector.get_books_genre() == {"Темная Башня": "Фантастика"}

    # Тесты get_books_for_children
    def test_get_books_for_children_valid_add_in_list(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.add_new_book("Оно")
        collector.set_book_genre("Гарри Поттер", "Фантастика")
        collector.set_book_genre("Оно", "Ужасы")
        assert collector.get_books_for_children() == ["Гарри Поттер"]

    def test_get_books_for_children_empty(self, collector):
        assert collector.get_books_for_children() == []

    # Тесты add_book_in_favorites
    def test_add_book_in_favorites_valid_name(self, collector):
        collector.add_new_book("Темная Башня")
        collector.add_book_in_favorites("Темная Башня")
        assert "Темная Башня" in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_non_exist_name(self, collector):
        collector.add_book_in_favorites("Книга Шпион")
        assert "Книга Шпион" not in collector.get_list_of_favorites_books()

    def test_cannot_add_duplicate_to_favorites(self, collector):
        collector.add_new_book("Темная Башня")
        collector.add_book_in_favorites("Темная Башня")
        collector.add_book_in_favorites("Темная Башня")
        assert collector.get_list_of_favorites_books() == ["Темная Башня"]

    # Тесты delete_book_from_favorites
    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book("Темная Башня")
        collector.add_book_in_favorites("Темная Башня")
        collector.delete_book_from_favorites("Темная Башня")
        assert "Темная Башня" not in collector.get_list_of_favorites_books()

    # get_list_of_favorites_books
    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.add_new_book("Властелин Колец")
        collector.add_book_in_favorites("Гарри Поттер")
        collector.add_book_in_favorites("Властелин Колец")
        assert collector.get_list_of_favorites_books() == ["Гарри Поттер", "Властелин Колец"]
