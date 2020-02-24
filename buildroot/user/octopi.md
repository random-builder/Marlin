
### octopi settings

### custom command: Leveling/Full Pass

```
G28 ; home/reset
G29 P1 ; measure
G29 P3.1 ; populate
G29 P5 C0.75 ; adjust
G29 T ; report
G29 A ; activate
G1 Z0 ; verify
```
