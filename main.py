import pymysql
from konlpy.tag import Okt, Mecab
mecab = Mecab(dicpath=r"C:/mecab/mecab-ko-dic")
Okt = Okt()

def nlp(example):
    stop_words = "안녕하세요 . ,"
    stop_words = set(stop_words.split(' '))

    ex = example.replace(" ","")
    word_tokens = Okt.morphs(ex)

    resultf = [word for word in word_tokens if not word in stop_words]

    result2 = ''.join(resultf)
    print(result2)
    nouns = mecab.nouns(result2)
    print('명사 단위:', nouns)

    conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='menuDB', charset='utf8')
    cur = conn.cursor()

    count = 0
    final_result = []
    for i in nouns:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='menuDB', charset='utf8')
        if count % 2 == 0:
            sql = "SELECT menuCode FROM menuTable where menu = %s"
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (nouns[count]))
                    result = cur.fetchone()
                    if result is None:
                        return 'false'
                    else:
                        for data in result:
                            final_result.insert(count, data)
                            print(data)

        elif count % 2 == 1:
            sql = "SELECT NumCode FROM NumTable where Num = %s"
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (nouns[count]))
                    result = cur.fetchone()
                    if result is None:
                        return 'false'
                    else:
                        for data in result:
                            final_result.insert(count, data)
                            print(data)

        count = count + 1
    final_result2 = ' '.join(final_result)
    print(final_result2)
    return final_result2


    #localhost8080/order?menu=26