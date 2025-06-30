# Row-based storage (Clickhouse style)
## Purpose
## Input
## Output
## Arch



# Column-based storage (Clickhouse style)
## Purpose
## Input
## Output
## Arch






















Based on your requirements and the architecture of PostgreSQL, here are the key components and concepts you should focus on for your simple row-oriented storage engine:

### 1. Heap File Management

You'll need a way to manage the file that stores your table's data. This file, often called a "heap file" in PostgreSQL, is organized into pages (or blocks) of a fixed size.

*   **Pages:** Divide your file into fixed-size blocks (e.g., 8KB, similar to PostgreSQL). A page is the smallest unit of I/O.
*   **Page Layout:** Within each page, you'll need a structure to store records. A simple approach is to have a header that tracks the number of records and a directory of pointers to the start of each record.
*   **File Extension:** You will need a mechanism to grow the file by adding new pages when the existing ones are full.

### 2. Record (Tuple) Management

This component deals with how individual records (rows) are stored within the pages of your heap file.

*   **Record Structure:** Since you're only supporting fixed-length strings, each record will have a simple, predictable size. A record will consist of a header and the data itself.
*   **Record Header:** The header can store metadata about the record, such as its visibility status (e.g., whether it has been deleted).
*   **Slotted Page Structure:** To manage records within a page, you can use a "slotted page" design. This involves an array of pointers (slots) at the beginning of the page that point to the actual records stored from the end of the page. This makes it easier to handle deletions and insertions without having to shift large amounts of data.

### 3. In-Memory Buffer/Cache Management

To avoid constant and slow disk I/O, you'll need a buffer manager. As mentioned in the PostgreSQL architecture, database operations are performed in a cache in shared memory.

*   **Buffer Pool:** This is a collection of in-memory frames, each of which can hold one page from your heap file.
*   **Page Pinning/Unpinning:** You'll need to "pin" a page in the buffer pool before it can be used and "unpin" it when you're done. This prevents a page from being evicted while it's in use.
*   **Page Eviction Policy:** When the buffer pool is full and a new page needs to be loaded, you'll need a policy (e.g., Least Recently Used - LRU) to decide which page to evict. If the evicted page is "dirty" (has been modified), it must be written back to disk.

### 4. Execution Engine (Physical Operators)

This is the core of your database's query processing. You'll implement the physical operators you specified:

*   **Table Scan:** This operator will iterate through all the pages and records in your heap file. For each page, it will load it into the buffer pool and then scan the records within that page.
*   **Insert:** This operator will find a page with enough free space, load it into the buffer pool, add the new record, mark the page as dirty, and then unpin the page.
*   **Delete:** This operator will find the record to be deleted, and instead of physically removing it, it will mark it as deleted in the record's header (a "soft delete"). This is a simplified version of how PostgreSQL handles deletes with MVCC.
*   **Filter:** This operator will take a stream of records from another operator (like a table scan) and apply a condition to each one, only passing through the records that meet the condition.
*   **Projection:** This operator will take a stream of records and select a subset of the columns (in your case, since you only have one string column, this would be a simple pass-through).
*   **Hash Aggregation:** For this operator, you'll need to create an in-memory hash table. As you iterate through the records from a child operator, you'll use the value of the string column as the key in the hash table and update the aggregate value (e.g., count).
*   


Based on the ClickHouse architecture and your requirements for a simple column-oriented storage engine, here are the key components you should implement using object-oriented programming:

### Core Storage Components

These classes form the foundation of your storage engine, managing how data is stored and accessed.

*   **`Column`**: Represents a single column of data in memory. Since you're only supporting fixed-length strings, this class will manage a contiguous block of memory or a list of strings.
    *   **Responsibilities**:
        *   Store an array or vector of fixed-length strings.
        *   Provide methods to add a new value (`append`), get a value at a specific index (`get`), and get a slice of values (`get_range`).
        *   Return the number of elements in the column (`size`).

*   **`Block`**: A container for a chunk of a table, holding data in-memory in a columnar format. This is the unit of data processing for your operators.
    *   **Responsibilities**:
        *   Hold a collection of `Column` objects, mapping column names to `Column` instances.
        *   Provide methods to add and retrieve columns by name.
        *   Keep track of the number of rows in the block.

*   **`DataPart`**: Represents a sorted segment of your data on disk. In your case, this could be a single file, or since you want a "file per table," this could be a logical section within that file.
    *   **Responsibilities**:
        *   Serialize and deserialize a `Block` of data to and from a portion of the table file.
        *   Maintain metadata about the part, such as the number of rows and the range of the primary key values.

*   **`MergeTree`**: The core of your storage engine, managing the lifecycle of `DataPart`s.
    *   **Responsibilities**:
        *   Handle the insertion of new data by creating new, sorted `DataPart`s.
        *   Implement the background merging logic: select multiple `DataPart`s, merge them into a new, larger `DataPart`, and atomically replace the old parts with the new one.
        *   For the `delete` functionality, you can introduce a hidden "is_deleted" column. During a merge, rows marked as deleted are discarded.

*   **`StorageEngine`**: The main entry point for interacting with a table.
    *   **Responsibilities**:
        *   Provide a single file to represent the table.
        *   Manage a collection of `DataPart`s.
        *   Orchestrate the `insert` and `delete` operations by interacting with the `MergeTree`.
        *   Provide an interface for the `TableScanOperator` to read data.

### Physical Plan Operators

These classes will represent the operations in your query execution plan. Each operator will consume and produce `Block`s of data.

*   **`Operator` (Abstract Base Class)**: Defines a common interface for all physical operators, with a `next()` method that returns the next `Block` of data.

*   **`TableScanOperator`**: Reads data from the `StorageEngine`.
    *   **Responsibilities**:
        *   Interact with the `StorageEngine` to get the relevant `DataPart`s for a query.
        *   Read `Block`s of data from the `DataPart`s sequentially.

*   **`InsertOperator`**: Inserts data into the `StorageEngine`.
    *   **Responsibilities**:
        *   Take a `Block` of data as input.
        *   Pass the `Block` to the `StorageEngine` to be written as a new `DataPart`.

*   **`FilterOperator`**: Filters rows based on a condition.
    *   **Responsibilities**:
        *   Take another operator as input (e.g., a `TableScanOperator`).
        *   For each `Block` from the input, apply a filtering condition and produce a new `Block` with only the rows that satisfy the condition.

*   **`ProjectionOperator`**: Selects a subset of columns.
    *   **Responsibilities**:
        *   Take another operator as input.
        *   For each `Block` from the input, create a new `Block` containing only the specified columns.

*   **`HashAggregationOperator`**: Performs aggregation (e.g., COUNT, SUM, AVG).
    *   **Responsibilities**:
        *   Take another operator as input.
        *   Maintain a hash table to store the state of the aggregation (e.g., group-by keys and intermediate aggregate values).
        *   Consume all `Block`s from the input, updating the hash table.
        *   Produce a final `Block` with the aggregated results.

*   **`HashJoinOperator`**: Joins two data streams.
    *   **Responsibilities**:
        *   Take two operators as input (left and right sides of the join).
        *   Build a hash table on the join key from one input (the "build" side).
        *   Stream `Block`s from the other input (the "probe" side), look up matching rows in the hash table, and produce joined `Block`s.

By implementing these components, you will have a solid foundation for a simple, yet powerful, column-oriented storage engine that follows the principles of the ClickHouse architecture.


to deepen my skills in storage engine. I want to implement  a simple column-oriented storage engine (clickhouse style, MergeTree):

just support string data type (fixed max length)

no additional index layer, just primary key, sorted key

no metadata/catalog management, just a file per table

use physical plan-level operator (insert, delete, tablescan, hash aggregation, filter, projection, hash join

what are components that I should implement (object oriented programming)?

https://clickhouse.com/docs/development/architecture