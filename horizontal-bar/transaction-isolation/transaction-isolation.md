# Transaction Isolation level
In SQL standard, concurrent transaction phenomena is that 
you don't want them to happen in some cases. To prevent them, you need to use a transaction isolation 
level high enough in exchange for lower performance.


Given context: two concurrent transaction A and B.

Remember: In postgres, row-level lock doesn't affect data querying at all 
(just affects on share-lock, share and key share and write-lock, key & no-key)

## 1. phenomena: dirty read
Previous Level: <strong> read uncommited </strong>

Define: transaction A read uncommited data of transaction B

Level: <strong> read commited </strong>

Postgresql Syntax (Default level):

    // In Postgres: read commited and read uncommited has the same effect
    begin transaction isolation level read committed;
    ...
    end;

##### How:

Postgres start each command with a new snapshot - current state of the table, 
include all committed transaction. So transaction only can read data commited 
or data uncommitted of itself.

## 2. Phenomena: non-repeatable read.
Previous level: read commited

Define: Transaction A read row X before and after when transaction B is finished. 
And see X has different values.

Level: repeatable read

Postgresql Syntax:
    
    begin transaction isolation level repeatable read;
    ...
    end;

##### how:

Postgres only use a snapshot at time transaction begin for all command within the transaction.
So transaction can't see any data change during the transaction. 

Transaction will have to wait other transaction that have lock on its target row finish first,
and will be rolled back if any of its target rows is deleted or updated.

## 3. phenomena: phantom read.
Previous level: read commited

Define: Transaction A target on a conditioned set of rows before and after when transaction B is finished.
And see the difference between two set.

Level: repeatable read

Postgresql Syntax:
    
    begin transaction isolation level repeatable read;
    ....
    end;

#### how:

Due to nature of repeatable read level, transaction A will see data or same set of target row
at the start of the transaction.

## 4. phenomena: serialization anomaly

Previous level: repeatable read

Define:

Level: serializable

Postgresql Syntax:

    begin transaction isolation level repeatable read;
    ....
    end;

##### how:

it works as same as repeatable level with extra monitoring for conditions use predicate locks. 
