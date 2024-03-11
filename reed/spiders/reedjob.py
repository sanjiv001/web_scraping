import scrapy

class ReedjobSpider(scrapy.Spider):
    name = "reedjob"
    page_number = 2
    allowed_domains = ["www.reed.co.uk"]
    start_urls = ["https://www.reed.co.uk/jobs/data-analyst-jobs"]

    def parse(self, response):
        # Extracting job information from current page
        job_articles = response.css('article.card.job-card_jobCard__MkcJD')

        for job_article in job_articles:
            job_url = job_article.css('a.job-card_jobCard__blockLink__PeeZx::attr(href)').get()
            title = job_article.css('a.job-card_jobCard__blockLink__PeeZx::text').get()
            salary = job_article.css('li.job-card_jobMetadata__item___QNud:nth-child(1)::text').get()
            location = job_article.css('li.job-card_jobMetadata__item___QNud:nth-child(2)::text').get()
            contract_type = job_article.css('li.job-card_jobMetadata__item___QNud:nth-child(3)::text').get()

            yield {
                'job_url': job_url,
                'title': title,
                'salary': salary,
                'location': location.strip(),
                'contract_type': contract_type.split(',')[0].strip(),
                'job_type': contract_type.split(',')[1].strip()
            }

        # Follow pagination link to the next page
        next_page = f'https://www.reed.co.uk/jobs/data-analyst-jobs?pageno={self.page_number}'
        if next_page:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
