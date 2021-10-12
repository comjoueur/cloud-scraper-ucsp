# Cloud Peru Forum Browser UCSP


## Requirements

- Install python dependencies:
  ```bash
  $ pip install -r requirements.txt
  ```

  - Set your AWS credentials and bucket

  `AWS_REGION_NAME`: put AWS region.
  `AWS_ACCESS_KEY_ID`: put your AWS key id.
  `AWS_SECRET_ACCESS_KEY`: put your AWS secret key access.
  `AWS_S3_BUCKET`: put bucket where will be saved all output and input files.

  Populate project input file data running spider:

  ```bash
  $ scrapy crawl forosperu
  ```

  Run hadoop project and paste output inverted index output in
  `assets/inverted_index` and page rank output in `assets/page_rank`

  Run django project with:

  ```bash
  $ python manage.py runserver
  ```

  Enter to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to see term search
