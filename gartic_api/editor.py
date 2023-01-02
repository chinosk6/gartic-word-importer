from . import api
import json
import typing as t


class GarticWordsEditor(api.GarticApi):
    def __init__(self, cookie: str, proxies=None):
        super().__init__(cookie, proxies)

    def get_subject_list(self):
        return json.loads(self.api_get_subjects().text)

    def edit_subject_words(self, language: int, subject: int, diff_index=0,
                           add_words: t.Optional[t.List[str]] = None, remove_words: t.Optional[t.List[str]] = None,
                           replace_all=False):
        if remove_words is None:
            remove_words = []
        subject_info = json.loads(self.api_get_subject_info(subject, language).text)
        need_remove_words = []
        for i in subject_info:
            word, dif_index = i
            if word in add_words:
                add_words.remove(word)
            if replace_all or (word in remove_words):
                need_remove_words.append(word)
        data = json.loads(self.api_edit_subject(language, subject, diff_index, add_words, need_remove_words).text)
        print("Edit Success" if data.get("return", False) else "Edit Failed!")
