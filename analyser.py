from typing import NoReturn
import re
from pymorphy3 import MorphAnalyzer
from wordcloud import WordCloud
from collections import Counter


class TextAnalyser:
    def __init__(
                self,
                source_file=None,
                destination_file='wordcloud.png',
                parts_of_speech=['NOUN'],
                words_ammount=100,
                wc_width=800,
                wc_height=600,
                wc_background='black',
                wc_margin=10
    ) -> None:
        ''' вызывает цепочку методов '''
        if source_file is None:
            raise Exception('Не указан файл для анализа!')
        self.source_file = source_file
        self.destination_file = destination_file
        self.read_file()
        self.check_empty_file()
        self.make_words()
        self.make_pos_words(parts_of_speech)
        self.make_top_words(words_ammount)
        self.make_wordcloud(wc_width, wc_height, wc_background, wc_margin)
        self.save_to_file()
        self.print_results()

    def read_file(self) -> None | NoReturn:
        ''' пытается открыть файл и считать его в строку '''
        try:
            with open(self.source_file, 'r', encoding='UTF-8') as file:
                self.file = file
                self.text = self.file.read()
        except FileNotFoundError:
            raise Exception(f'Файл {self.source_file} не найден!')

    def check_empty_file(self) -> None | NoReturn:
        ''' проверяет пустой ли файл '''
        if not self.text:
            raise RuntimeError(f'Файл {self.source_file} пуст! Попробуйте другой файл.')

    def make_words(self) -> None:
        ''' делает буквы текста строчными, создает список слов '''
        self.text = self.text.lower()
        self.words = re.findall(r'\b[а-яё-]+\b', self.text)

    def make_pos_words(self, parts_of_speech) -> None:
        ''' делает список из подходящих частей речи '''
        morph = MorphAnalyzer()
        self.pos_words = []
        for word in self.words:
            parses = morph.parse(word)
            parse = parses[0]
            if any(pos in parse.tag for pos in parts_of_speech):
                self.pos_words.append(parse.normal_form)
        if not self.pos_words:
            raise RuntimeError('В тексте не нашлось подходящих частей речи.')

    def make_top_words(self, words_ammount):
        '''
        создает словарь вида:
        слово: количество упоминаний
        '''
        self.pos_words
        counter = Counter(self.pos_words)
        self.counted_words = dict(counter.most_common(words_ammount))

    def make_wordcloud(self, wc_width, wc_height, wc_background, wc_margin) -> None:
        ''' создает объект облака слов '''
        self.wordcloud = WordCloud(
            width=wc_width,
            height=wc_height,
            background_color=wc_background,
            margin=wc_margin,
            scale=1
        ).generate_from_frequencies(self.counted_words)

    def save_to_file(self) -> None:
        ''' сохраняет объект облака слов в файл-изображение '''
        try:
            self.wordcloud.to_file(self.destination_file)
        except:
            raise RuntimeError(
                'Не удалось сохранить изображение облака слов в файл!'
            )

    def print_results(self) -> None:
        ''' выводит отчет на экран '''
        print(f'В этом тексте {len(self.words)} слов')
        print(f'Подходящих частей речи: {len(self.pos_words)}')
        print(f'Изображение сохранено в файл {self.destination_file}')


if __name__ == '__main__':
    TextAnalyser(source_file='text.txt', parts_of_speech=['NOUN', 'VERB'])