# Example Document with Mermaid Diagrams

This is an example markdown document containing various Mermaid diagrams that can be converted to PNG using the MermaidToPNG converter.

## Flowchart Example

```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process 1]
    B -->|No| D[Process 2]
    C --> E[End]
    D --> E
```

## Sequence Diagram Example

```mermaid
sequenceDiagram
    participant User
    participant System
    participant Database
    
    User->>System: Login Request
    System->>Database: Validate Credentials
    Database-->>System: Validation Result
    System-->>User: Login Response
```

## Class Diagram Example

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +speak()
    }
    
    class Dog {
        +String breed
        +bark()
    }
    
    class Cat {
        +int lives
        +meow()
    }
    
    Animal <|-- Dog
    Animal <|-- Cat
```

## Gantt Chart Example

```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    section Development
    Design      :active, des1, 2025-01-01, 30d
    Implementation :des2, after des1, 45d
    Testing     :des3, after des2, 30d
    section Deployment
    Production  :crit, dep1, 2025-03-15, 15d
```

## Pie Chart Example

```mermaid
pie title Programming Language Usage
    "Python" : 45
    "JavaScript" : 30
    "Java" : 15
    "Other" : 10
```

## State Diagram Example

```mermaid
stateDiagram-v2
    [*] --> Still
    Still --> [*]
    
    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]
```

## Complex Flow Example

```mermaid
graph LR
    A[Start] --> B{Input Validation}
    B -->|Valid| C[Process Data]
    B -->|Invalid| D[Show Error]
    C --> E{Data Analysis}
    E -->|Success| F[Generate Report]
    E -->|Failure| G[Log Error]
    F --> H[End]
    D --> H
    G --> H
```

## Usage Instructions

To convert these diagrams to PNG, run:

```bash
# Using Python script (requires Node.js)
python mermaid_to_png_converter.py example_document.md

# Using standalone executable
./mermaid_to_png_converter example_document.md
```

The tool will create an `example_document_diagrams/` directory containing:
- `.mmd` files with the extracted Mermaid code
- `.png` files with the generated images

Each diagram will be numbered sequentially (diagram_1, diagram_2, etc.).
