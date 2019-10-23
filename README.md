# Zen Desk -> Google Sheets

Pulls a list of College Track Zen Desk Help Desk articles and populates a Google sheet for manual review of what needs to be updated.

### Prerequisites

```
python 3.7
conda 4.7.12
```

### Installing

```
conda env create -f environment.yml
conda activate env
```
Create a `.env` file in the root of the project and insert your key/value pairs in the following format of KEY=VALUE:

```
ZD_USERNAME=<your zd username>
ZD_PASSWORD=<your zd password>
```


