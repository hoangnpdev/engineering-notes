# Data normalization

Relations not following data normalization do have redundancy in their data.
This causes inconvenience and inconsistency during operating: updating, deleting.
<br><br>
Higher level of normalization, less redundancy in data, more complex relation schema, worse query performance

## 1NF

Conditions: 

- There's no non-atomic attribute
- There's no duplicate row or each row has a primary key

Redundancy, Inconvenience, Inconsistency:
- update value in group, array type attribute
- has duplicate row

## 2NF

Conditions:
- 1NF
- There's no functionally dependency of non-prime attribute on any part of candidate key.

Redundancy, Inconvenience, Inconsistency:
- redundancy on pair of (non-prime attribute, part of candidate key) that have functionally dependency

## 3NF
Conditions:
- 2NF
- There's no functionally dependency of non-prime attribute on any other non-prime attribute.

Redundancy, Inconvenience, Inconsistency:
- redundancy on pair of (two non-prime attributes) that have functionally dependency


## BCNF

Conditions:
- 3NF
- no attribute functionally depend on a set that is not a candidate key

Example 
(street_address, city) -> zip_code
zip_code -> street_address