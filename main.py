import gartic_api
import json
from tkinter import filedialog, Tk

LANGUAGE_ID = 16  # 简体中文/Simplified Chinese

cookie = input("请输入您的Cookie: ").strip()
proxy_url = input("HTTP 代理 URL (不需要代理请留空): ").strip()
proxies = {
    "http": proxy_url,
    "https": proxy_url
} if proxy_url else None

gapi = gartic_api.GarticWordsEditor(cookie, proxies)
language_dict = json.loads(gapi.api_get_lang(LANGUAGE_ID).text)

def get_subject_name_from_id(subject_id):
    return language_dict["subjects"].get(str(subject_id), f"无效主题ID: {subject_id}")

def get_words_from_txt():
    tk_root = Tk()
    tk_root.withdraw()
    path = filedialog.askopenfilename(title="请选择词库文件, 词语一行一个")
    tk_root.destroy()
    with open(path, "r", encoding="utf8") as f:
        textlst = f.read().replace("\r", "").split("\n")
    while True:
        try:
            textlst.remove("")
        except:
            break
    return textlst

def get_self_subjects(need_print=False):
    subject_list = gapi.get_subject_list()
    lang_subject_ids = []
    n = 0
    for lang_id in subject_list:
        for subject_id in subject_list[lang_id]:
            if need_print:
                print(f"[{n}] 语言ID: {lang_id}, 主题: {get_subject_name_from_id(subject_id)}")
            lang_subject_ids.append([int(lang_id), int(subject_id)])
            n += 1
    return lang_subject_ids


def create_new_subject():
    for subject_id in language_dict["subjects"]:
        print(f"主题ID: {subject_id}, 主题内容: {get_subject_name_from_id(subject_id)}")
    target_subject_id = int(input("请输入想添加的主题ID (注意, 若主题已存在, 将直接清除原内容): ").strip())
    diff_index = int(input("请输入难度 0-简单, 1-正常, 2-困难: ").strip())
    gapi.edit_subject_words(LANGUAGE_ID, target_subject_id, diff_index, get_words_from_txt(), replace_all=True)


def edit_subject():
    subject_list = get_self_subjects(need_print=True)
    edit_index = int(input("请输入需要编辑主题序号: ").strip())
    if edit_index >= len(subject_list):
        print("输入的序号不合法")
        return edit_subject()
    lang_id, subject_id = subject_list[edit_index]
    diff_index = int(input("请输入难度 0-简单, 1-正常, 2-困难: ").strip())
    gapi.edit_subject_words(lang_id, subject_id, diff_index, get_words_from_txt())


def main():
    do_type = input("[1] 创建新主题\n"
                    "[2] 添加新词到现有主题\n"
                    "\n请选择您的操作: ").strip()
    do_func = {
        "1": create_new_subject,
        "2": edit_subject
    }
    if do_type in do_func:
        do_func[do_type]()
    else:
        print("???")


if __name__ == "__main__":
    while True:
        main()
        print("\n")
