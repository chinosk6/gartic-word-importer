import json
import requests
import typing as t


class GarticApiError(Exception):
    pass


def dec_response_checker(valid_status_codes: t.Optional[t.List[int]] = None):
    if valid_status_codes is None:
        valid_status_codes = [200]

    def inner(func: t.Callable[..., requests.Response]):
        def _(*args, **kwargs):
            ret = func(*args, **kwargs)
            if ret.status_code not in valid_status_codes:
                raise GarticApiError(f"API Error ({ret.status_code}): {ret.text}")
            return ret
        return _
    return inner


class GarticApi:
    def __init__(self, cookie: str, proxies=None):
        self.base_url = "https://gartic.io"
        self.cookie = cookie
        self.proxies = proxies

    def _get_base_headers(self):
        return {
            'Referer': 'https://gartic.io/rooms',
            'Cookie': self.cookie,
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46'
        }

    def _do_get(self, path: str, headers=None, params=None, **kwargs):
        req_headers = self._get_base_headers()
        if headers is not None:
            req_headers.update(headers)
        response = requests.request("GET", f"{self.base_url}{path}", params=params, headers=req_headers,
                                    proxies=self.proxies, **kwargs)
        return response

    def _do_post_json(self, path: str, headers=None, params=None, json_data=None, **kwargs):
        req_headers = self._get_base_headers()
        req_headers["Content-Type"] = "application/json"
        if headers is not None:
            req_headers.update(headers)
        response = requests.request("POST", f"{self.base_url}{path}", params=params, headers=req_headers,
                                    data=json.dumps(json_data), proxies=self.proxies, **kwargs)
        return response

    @dec_response_checker(valid_status_codes=[200, 304])
    def api_get_subjects(self):
        return self._do_get("/req/subjects")

    @dec_response_checker()
    def api_get_subject_info(self, subject: int, language: int):
        return self._do_get("/req/subject", params={"subject": subject, "language": language})

    @dec_response_checker()
    def api_edit_subject(self, language: int, subject: int, diff_index=0,
                         add_words: t.Optional[t.List[str]] = None, remove_words: t.Optional[t.List[str]] = None):
        data = {
            "language": language,
            "subject": subject,
            "added": [[i, diff_index] for i in add_words] if add_words is not None else [],
            "removed": [] if remove_words is None else remove_words
        }
        return self._do_post_json("/req/editSubject", json_data=data)

    @dec_response_checker(valid_status_codes=[200, 304])
    def api_get_lang(self, lang_id: int):
        return self._do_get("/req/lang", params={"id": lang_id})
