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
    - file.folder == "projects/P1-(⚡blitz)__  get a job/P1A-saptak.github.io/P1A1-notes"
views:
  - type: table
    name: Table
    groupBy:
      property: sidequest
      direction: ASC
    order:
      - is-task
      - file.name
      - status
      - 🌄P-TYPE
      - project
      - sidequest
      - tags
    sort:
      - property: project
        direction: DESC
      - property: 🌄P-TYPE
        direction: DESC
      - property: tags
        direction: ASC
    columnSize:
      note.task: 89
      file.name: 435
      note.status: 124
      note.🌄P-TYPE: 163
      note.project: 357
  - type: tasknotesKanban
    name: kanban board
    filters:
      and:
        - is-task == true
    sort: []
  - type: list
    name: all-list
    groupBy:
      property: sidequest
      direction: ASC
    indentProperties: true
    markers: none
  - type: tasknotesTaskList
    name: task-list
    filters:
      and:
        - is-task == true
    groupBy:
      property: sidequest
      direction: ASC

```


