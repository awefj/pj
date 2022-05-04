import os
import hashlib
from collections import defaultdict
import datetime


class reader:
    """
    this class provides methods that collect file& directory list
    """

    def __init__(self, directory=None):
        if directory is None:
            self._dir = None
        else:
            self._dir = self.check_directory_list(directory)

        self.items = defaultdict(list)

        self.size_count = 0
        self.item_count = 0

        self.same_size_count = 0
        self.same_size_item_count = 0

    @staticmethod
    def check_directory_list(dirs):
        """
        check dirs if exists and removes child directory.
        :return lists of directory
        """
        temp = []
        nums = []
        result = []
        # check dirs exists
        for directory in dirs:
            if os.path.exists(directory):
                temp.append(directory)
        temp.sort()

        for i in range(len(temp)):
            for j in range(i + 1, len(temp) - i):
                if temp[i] in temp[j]:
                    print(f"dir {temp[i]} is parent of dir {temp[j]}")
                    nums.append(j)
        nums.sort(reverse=True)
        for num in nums:
            temp.pop(num)
        for item in temp:
            result.append(os.path.abspath(item))
        print(f"processed directory list : {result}")
        return result

    def get_items_by_size(self):
        """
        get item list from multiple directories.
        """
        for directory in self._dir:
            for root, directories, files in os.walk(directory):
                for filename in files:
                    path = os.path.join(root, filename)
                    try:
                        file_size = os.path.getsize(path)
                        self.items[file_size].append(path)
                        self.item_count += 1
                    except(OSError,):
                        print(f"----cannot read {path} ----")
                        continue
        self.size_count = len(self.items)

    def get_items_by_size_dupe(self):
        """
        remove files that don't have same sized one
        """
        temp = defaultdict(list)
        for file_size in self.items:
            if len(self.items[file_size]) == 1:
                continue
            for item in self.items[file_size]:
                temp[file_size].append(item)
                self.same_size_item_count += 1
        self.same_size_count = len(temp)
        self.items = temp

    def print_items_by_size(self):
        """
        print list from items_by_size
        """
        for file_size in self.items:
            print(f"size : {file_size}")
            for item in self.items[file_size]:
                print(f"\t{item}")

    def clear(self):
        self.items = defaultdict(list)

        self.size_count = 0
        self.item_count = 0

        self.same_size_count = 0
        self.same_size_item_count = 0


class hash_comp(reader):
    """
    this class provides methods that process file hash values to evaluate file is duplicate.
    """

    def __init__(self, directory=None, fast=False):
        super().__init__(directory)
        self.hash1k = defaultdict(list)
        self.hash = defaultdict(list)

        self.is_fast = fast

        self.hash1k_count = 0
        self.hash1k_item_count = 0

        self.same_hash1k_count = 0
        self.same_hash1k_item_count = 0

        self.hash_count = 0
        self.hash_item_count = 0

        self.same_hash_count = 0
        self.same_hash_item_count = 0

    def set_param(self, directory, fast):
        """

        :param directory:
        :param fast:
        """
        self._dir = self.check_directory_list(directory)
        self.is_fast = fast

    @staticmethod
    def get_hash(file_location, size=0, hash_algorithm=hashlib.sha1):
        """
        read the file and returns hashing string
        :param file_location: file location
        :param size: file size for using at hashing
        :param hash_algorithm: hashing algorithm
        :return: hashing string
        """
        hash_algo = hash_algorithm()
        file = open(file_location, 'rb')  # open file in read & binary mode
        try:
            if size == 0:
                hash_algo.update(file.read())
            else:
                hash_algo.update(file.read(size))
        except(OSError,):
            print(f"failed to hash {file_location}")
        finally:
            file.close()
        hash_val = hash_algo.digest()  # get result
        return hash_val

    def get_hash_1k_list(self):
        """
        get hash list from self.same_sized_items
        """
        for size in self.items:
            for item in self.items[size]:
                self.hash1k[(size, self.get_hash(item, 1024))].append(item)
                self.hash1k_item_count += 1
        self.hash1k_count = len(self.hash1k)

        if self.same_size_item_count != self.hash1k_item_count:
            print("get_hash_1k_list - anomaly detected")

    def get_same_hash_1k_list(self):
        """
        get only same hash values from self.hash1k
        """
        temp = defaultdict(list)
        # self.get_hash_1k_list()
        for size_hash_1k in self.hash1k:
            if len(self.hash1k[size_hash_1k]) == 1:
                continue
            for item in self.hash1k[size_hash_1k]:
                temp[size_hash_1k].append(item)
                self.same_hash1k_item_count += 1
        self.same_hash1k_count = len(temp)
        self.hash1k = temp

    def get_same_hash_1k_list_(self):
        """
        removes which don't have same hash values from the self.hash1k
        """
        # self.get_hash_1k_list()
        removal = list()
        count = self.hash1k_item_count
        for size_hash_1k in self.hash1k:
            if len(self.hash1k[size_hash_1k]) == 1:
                removal.append(size_hash_1k)
        for target in removal:
            self.hash1k.pop(target)
            count -= 1
        self.same_hash1k_item_count = count
        self.same_hash1k_count = len(self.hash1k)

    def get_hash_list(self):
        """
        get hashing list from self.hash1k
        """
        for size_hash_1k in self.hash1k:
            for item in self.hash1k[size_hash_1k]:
                self.hash[(size_hash_1k[0], self.get_hash(item))].append(item)
                self.hash_item_count += 1
        self.hash_count = len(self.hash)

    def get_same_hash_list(self):
        """
        get only same hash values from self.hash
        """
        temp = defaultdict(list)
        # self.get_hash_list()
        for size_hash in self.hash:
            if len(self.hash[size_hash]) == 1:
                continue
            for item in self.hash[size_hash]:
                temp[size_hash].append(item)
                self.same_hash_item_count += 1
        self.same_hash_count = len(temp)
        self.hash = temp

    def get_same_hash_list_(self):
        """
        removes which don't have same hash value from the self.hash
        """
        # self.get_hash_list()
        count = self.hash_count
        removal = list()
        for size_hash in self.hash:
            if len(self.hash[size_hash]) == 1:
                removal.append(size_hash)
        for target in removal:
            self.hash.pop(target)
            count -= 1
        self.same_hash_item_count = count
        self.same_hash_count = len(self.hash)

    def print_hash_compared_items(self):
        """
        print list of self.hash1k or self.hash
        """
        ptr = self.hash1k
        filecount = 0

        if not self.is_fast:
            ptr = self.hash
        print(f"is fast : {self.is_fast}")
        for size_hash in ptr:
            print(f"size : {size_hash[0]}\nhash : {size_hash[1]}\ncount : {len(ptr[size_hash])}")
            filecount += len(ptr[size_hash])
            for file in ptr[size_hash]:
                print(f"\t\tfile : {file}")
        print(f"hash count : {len(ptr)}\nfile count : {filecount}")

    def print_count(self):
        """
        print count of each lists
        """
        print(f"all sizes\t: {self.size_count} \titems : {self.item_count}")
        print(f"same sized\t: {self.same_size_count} \titems : {self.same_size_item_count}")
        print(f"all 1k\t: {self.hash1k_count} \titems : {self.hash1k_item_count}")
        print(f"same 1k\t: {self.same_hash1k_count} \titems : {self.same_hash1k_item_count}")

        if not self.is_fast:
            print(f"all hash\t: {self.hash_count}, \titems : {self.hash_item_count}")
            print(f"same hash\t: {self.same_hash_count}, \titems : {self.same_hash_item_count}")

    def time_stamp(self):
        """
        run all functions & print timestamps
        """
        _start = datetime.datetime.now()
        self.get_items_by_size()
        print(f"getItems : {datetime.datetime.now() - _start}")

        start = datetime.datetime.now()
        self.get_items_by_size_dupe()
        print(f"getSameSizeItems : {datetime.datetime.now() - start}")

        start = datetime.datetime.now()
        self.get_hash_1k_list()
        print(f"get1kList : {datetime.datetime.now() - start}")

        start = datetime.datetime.now()
        self.get_same_hash_1k_list()
        print(f"get1kDupeList : {datetime.datetime.now() - start}")

        if not self.is_fast:
            start = datetime.datetime.now()
            self.get_hash_list()
            print(f"getHashList : {datetime.datetime.now() - start}")

            start = datetime.datetime.now()
            self.get_same_hash_list()
            print(f"getDupeList : {datetime.datetime.now() - start}")

        print(f"total : {datetime.datetime.now() - _start}")

    def get_result(self):
        """
        returns duplicate file list.
        :return: self.hash or self.hash1k
        """
        self.time_stamp()
        if not self.is_fast:
            return self.hash
        return self.hash1k

    def clear(self):
        super().clear()
        self.hash1k = defaultdict(list)
        self.hash = defaultdict(list)

        self.is_fast = False

        self.hash1k_count = 0
        self.hash1k_item_count = 0

        self.same_hash1k_count = 0
        self.same_hash1k_item_count = 0

        self.hash_count = 0
        self.hash_item_count = 0

        self.same_hash_count = 0
        self.same_hash_item_count = 0
