mermaid
graph LR
  subgraph API Gateway [API Gateway]
    h1[User Interface] -->|Account Inquiries & Transactions| a(API Gateway)
  end
  subgraph Core Banking [Core Banking System]
    a -->|Account Validation & Processing| b(Core Banking)
    b -->|Account Balances & Transaction History| c(Core Banking)
    b -->|Funds Transfer & Deposits| d(Core Banking)
  end
  subgraph Data Persistence [Data Persistence Layer]
    b -->|Read & Write Account Data| e(Data Persistence)
    c -->|Read Account Data| e
    d -->|Update Account Data| e
  end
  subgraph External Systems [External Systems]
    d(Core Banking) -->|External Payment Processing| f
  end
  a <--|Account Information & Transaction Results| h1
  f -->|Payment Confirmation/Rejection| d
