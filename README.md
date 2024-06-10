graph LR
  A[User Interface] --> B{Presentation}
  B --> C{Business Logic}
  C --> D{Data Access}
  D --> E[Database]
  C --> F{Security}
  F --> B
  B --> A
  
  subgraph Data Access
    D --> D1{Account table}
    D --> D2{Transaction table}
  end
