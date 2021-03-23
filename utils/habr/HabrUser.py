import requests
import bs4


def tags_image_user(profile: str):
    try:
        res = requests.get('https://habr.com/ru/users/' + profile.strip() + '/')
    except requests.exceptions.RequestException as e:
        print(e.errno)
        return [-1]

    html_data = bs4.BeautifulSoup(res.text, 'html.parser')
    if res.status_code != 200:
        return [404]

    return [0]
    # all_images = html_data.find_all('img')
    # image_url = all_images[0].attrs["src"]
    # filename = 'avatar.png'
    # if image_url[:4] != 'http':
    #     image_url = 'http:' + image_url
    # img_data = requests.get(image_url)
    #
    # with open(filename, 'wb') as fd:
    #     for chunk in img_data.iter_content(1):
    #         fd.write(chunk)
    #
    # finded_posts = html_data.find_all(class_='profile-section__user-hub')  # Nightly нет секции тегов
    # tag_list = list()
    # for paragraph in finded_posts:
    #     tag_list.append(paragraph.contents[0])
    #
    # if len(tag_list) == 0:
    #     return [0]
    # return tag_list


def get_user_tags(profile: str) -> list:
    event_dict = {-1: 'HABR_CONNECTION_ERROR',
                  404: 'NO_PROFILE', }
    user_tag_list = tags_image_user(profile)
    if user_tag_list[0] in event_dict.keys():
        return False
    return True
