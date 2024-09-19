import random
import string

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



class Utils:
    @staticmethod
    def id_generator(size=6, salt=""):
        prefix = ""
        if salt:
            import hashlib

            prefix = int(hashlib.sha1(salt.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
        ran_str = "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))
        return f"{prefix}{ran_str}"

    @staticmethod
    def paginator(data, page=1, per_page=10, total_count=None):
        paginator = CustomPaginator(data, per_page, total_count)
        return paginator.paging(page), paginator.count

    @staticmethod
    def compare_dicts(dict1, dict2):
        differing_keys = []
        differing_dict = {}

        for key in dict1.keys():
            if key in dict2 and dict1[key] != dict2[key]:
                differing_keys.append(key)
                differing_dict[key] = (dict1[key], dict2[key])

        for key in dict2.keys():
            if key not in dict1:
                differing_keys.append(key)
                differing_dict[key] = (None, dict2[key])

        return differing_keys, differing_dict

class CustomPaginator(Paginator):
    def __init__(self, object_list, per_page, total_count):
        super().__init__(object_list, per_page)
        self.set_total_count(total_count)

    def set_total_count(self, total_count=None):
        # Prevent one more query get total count inside Paginator
        # It's expensive when we do paging on a large table
        if total_count:
            setattr(self, "count", total_count)

    def paging(self, page):
        try:
            result = self.page(page)
        except PageNotAnInteger:
            result = self.page(1)
        except EmptyPage:
            result = self.page(self.num_pages)
        return list(result)
