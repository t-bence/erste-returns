# erste-returns

Computes returns on investments at Erste Hungary

Especially designed for Hungarian users, as it lets you track the return from two sources:

- from the investment value, and
- from the EUR/HUF exchange rate

Input: you need to save your current holdings from the Erste brokerage website.

## Some code snippets

```[python]
import lxml.html
doc = lxml.html.parse("EURHUF.html")

print(doc.xpath("//tr/td[1]/text()")) # get dates
print(doc.xpath("//tr/td[2]/text()")) # get rates
```
