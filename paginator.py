from rest_framework.pagination import LimitOffsetPagination


class ClassPaginator(LimitOffsetPagination):
    page_size = 20  # Limite à 15 éléments par page
    page_size_query_param = 'page_size'
    max_page_size = 100
    default_limit = 20  # Définit une limite par défaut si aucun paramètre `limit` n'est fourni
    max_limit = 100 
