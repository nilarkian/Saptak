---
id: 2026MayW1906Wed1012pm59
area:
tags: []
project:
  - "[[notes]]"
dateCreated: "[[2026-05-06]]"
---


```base
filters:
  or:
    - project == ["[[notes]]"]
    - file.folder == "projects/P1-(⚡blitz)__  get a job/P1A-saptak.github.io/P1A1-notes"
formulas:
  created: (file.ctime).format("Do MMM")
views:
  - type: table
    name: Table
    order:
      - formula.created
      - file.name
      - layout
      - is_note
      - project
      - tags
    sort:
      - property: file.ctime
        direction: DESC
    columnSize:
      formula.created: 66
      file.name: 581
      note.project: 357
  - type: tasknotesKanban
    name: kanban board
    filters:
      and:
        - is-task == true
    groupBy:
      property: status
      direction: ASC
    sort: []

```



