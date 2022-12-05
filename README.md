# if3140-tubes2

# Optimistic Concurrency Control / Validation Base Protocol

## How to Run
```
cd OCC
```
```
python Schedule.py input1.txt
```

## Test Case
- input1.txt: valid schedule
- input2.txt: invalid schedule, intersect operation
- input3.txt: invalid schedule, Ti<Tj and Tj complete write after Ti start validation phase
