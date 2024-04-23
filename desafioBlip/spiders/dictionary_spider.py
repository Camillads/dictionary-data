
import scrapy

class DictionarySpider(scrapy.Spider):
    name = 'dictionary'
    start_urls = ['https://dicionariocriativo.com.br']

    def parse(self, response):
        urls_words = response.css('.tags li a::attr(href)').getall()

        for url_word in urls_words:
            yield scrapy.Request(url_word, callback=self.parse_dictionary)

    def parse_dictionary(self, response):
        word = response.url.split('/')[-1]
        synonyms = response.css('section#sinant .contentListData p:nth-child(1) a::text').getall()
        antonyms = response.css('section#sinant .contentListData p:nth-child(2) a::text').getall()
        ul_tags = response.css('div.resumoBoxContent section.auleteResult ul')
        
        phrases = []
        for ul_tag in ul_tags:
            a_texts = ul_tag.css('li a::text').getall()
            full_text = ' '.join(a_texts).strip()
            phrases.append(full_text)

        yield {
            'word': word,
            #'meaning': phrases,
            'synonyms': synonyms,
            'antonyms': antonyms
        }        

        for synonym in synonyms:
            yield scrapy.Request(f'https://dicionariocriativo.com.br/{synonym}', callback=self.parse_word)
        
        for antonym in antonyms:
            yield scrapy.Request(f'https://dicionariocriativo.com.br/{antonym}', callback=self.parse_word) 

    def parse_word(self, response):
        word = response.url.split('/')[-1]
        synonyms = response.css('section#sinant .contentListData p:nth-child(1) a::text').getall()
        antonyms = response.css('section#sinant .contentListData p:nth-child(2) a::text').getall()
        ul_tags = response.css('div.resumoBoxContent section.auleteResult ul')
        
        phrases = []
        for ul_tag in ul_tags:
            a_texts = ul_tag.css('li a::text').getall()
            full_text = ' '.join(a_texts).strip()
            phrases.append(full_text)

        yield {
            'word': word,
            #'meaning': phrases,
            'synonyms': synonyms,
            'antonyms': antonyms
        }   