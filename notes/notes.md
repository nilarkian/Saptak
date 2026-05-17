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
    - project.contains(this.file.name)
    - file.folder.contains(this.file.name)
formulas:
  created: (file.ctime).format("Do MMM")
views:
  - type: table
    name: Table
    groupBy:
      property: file.folder
      direction: ASC
    order:
      - is-task
      - formula.created
      - file.name
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



