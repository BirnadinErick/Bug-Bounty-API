# Bug-Bounty-API
A :beetle: tracking Flask based API with No-SQL database integration.

## Glossary
##### Project Bug Bounty uses its own naming conventions, they as follows:-
```
- Bug     --> bugs, issues in the solutions
- Bounty  --> a project is characterized as a bounty
- Clan    --> a project team is a clan
- Hunter  --> each user ia a hunter, who hunts down bugs in a bounty, a member of a/more clan/s
```
#### Elaboration
##### 1) Bug
A **Bug** is an issue or a bug in your current solution that is associated with the ***Bounty*** a bug is included currently. A **Bug** can be resided in **a**
***Bounty***. A **Bug** has attributes such as:
  ```c++
    int::b_id         // immutable unique id
    char[]::bname     // immutable name for a/an bug/issue
    int::author       // immutable unique hunter id who spot the bug for the first time
    bool::status      // muttable two state status indicating whether the bug is open or closed using 1 or 0 ints
    float::cstamp     // immutable POSIX timestamp corresponding the origin of the bug in the server(not that much accurate)
    int::bo_id        // mutable bounty id bug is related to
    char[]::desc      // extra info about the bug
    int[]::assignees  // muttable var. length array of ints whom this bug is assigned to 
  ```
- Here `Bug::status` is changed accordingly using `/bug --> PATCH`

##### 2) Hunter
A **Hunter** is just an alleged user in the system who can create bugs, clans, bounties etc. A **Hunter** becomes a leader when the **Hunter** creates a ***Clan*** and has
some privileges inside that ***Clan***. A **Hunter** can have many ***Clan***s as well as participate in many as well. A **Hunter** has attributes such as:
  ```c++
    int::h_id         // immutable unique id
    char[]::hname     // immutable name for the hunter
    char[]::phash     // mutable hash in binary string for the passwd of the hunter
    float::cstamp     // immutable POSIX timestamp corresponding the origin of the hunter in the server(not that much accurate)
    int[]::c_ids      // muttable var. length array of ints relating hunter to various clans
    int[]::b_ids      // muttable var. length array of ints relating hunter to various bounties
  ```

##### 3) Clan
A **Clan** is just a ___Team___ consists of one/many ***Hunter***/s that occurs within a ***County***(more on ***County*** later).
A **Clan** can have a/many ***Bounty***/s associated
with it, **but** a ***Bounty*** can ONLY have 1 **Clan** associated with it.
A **Clan** has attributes such as:
  ```c++
    int::c_id         // immutable unique id
    char[]::cname     // immutable name for the clan
    float::cstamp     // immutable POSIX timestamp corresponding the origin of the clan in the server(not that much accurate)
    int[]::ls         // muttable var. length array of ints relating clan to particular leader/s
    int[]::hs         // muttable var. length array of ints relating clan to a/various hunter/s
    int[]::bs         // muttable var. length array of ints relating clan to a/various bounty/s
  ```
- A `Clan::Leader` is like an admin to the **Clan** who has more privileges to the **Clan** than normal **Hunter**/s


## Structure
The struture of this project is ***custom***. Scripts are divided into different folders according to their puprpose and types. 
The current(**as of May 04, 2021**) is as follows and may be changed par purpose:-
  
  ```
  API/
   
    -- app.py                         : main script that initalized the API
  
    -- .gitignore,LICENSE, README.md  : usual git files and others
   
    -- utility/                       : utility func.s and helpers
    
      -- .env                         : this is where your .env file should be if const.py is not configured
   
      -- const.py                     : most of the const are saved here in one place
   
      -- mongo_api.py                 : mongo API object resided here and intialized here
  
      -- helpers.py                   : helper func.s to create a unique id, hash passwd etc.
   
      -- exceptions.py                : custom exceptions
   
    -- resources/                     : resource object for flask_restful modules
   
      -- resource_bounty.py           : resource object for /bounty API endpoint
      
      -- resource_bug.py              : resource object for /bug API endpoint
      
      -- resource_clan.py             : resource object for /clan API endpoint
      
      -- resource_hunter.py           : resource object for /hunter API endpoint

```

## Technology
Project Bug Bounty is a collection of client-and-server softwares in :beetle: tracking system. And this repository contains the backend API of the system.
Bug Bounty uses [Flask](https://flask.palletsprojects.com/en/1.1.x/) (a [Python](https://www.python.org/) based web framework) as RESTful API and [MongoDB](https://www.mongodb.com/what-is-mongodb)
as Database Server.

#### Thank you for looking into this.
Code with ♥, Birnadin Erick🖐,
May 2021.












