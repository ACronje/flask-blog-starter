# Flask blog starter project

Blog application built with [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [SQLAlchemy](https://www.sqlalchemy.org/).

## Get started

Start by setting up your development environment. First, make sure that you have _Python 3.7.1_ or later available in your terminal. The easiest way to manage multiple versions of _Python_ is to use [pyenv](https://github.com/pyenv/pyenv).

Next, in your project root, install the Python dependencies by executing:

```
make dev_install
```

then run the application by executing:

```
make run
```

now you can access your application by navigating to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

## Linting

To lint your Python code using _flake8_ run:

```
make lint
```

## Testing

Run the automated tests by executing:

```
make test
```

## GraphQL

This starter features a GraphQL API built with [graphene](https://github.com/graphql-python/graphene). To access the GraphiQL of your running server navigate to [http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql) in your browser.

### Fetch all posts

To fetch all posts execute the following query in GraphiQL:

```
{
  posts {
    edges {
      node {
        id
        title
        content
        createdAt
      }
    }
  }
}
```

### Filter posts by tag name and creation date

To filter posts by tag name and/or creation date, execute the following query in GraphiQL:

```
{
  posts(tagName: "tech", date: "2021-04-04") {
    edges {
      node {
        id
        title
        content
        createdAt
        tagNames
      }
    }
  }
}
```
Note that the date must be in iso8601 format.

### Authenticating against the graphql CUD mutations

The graphql post Create, Update, and Delete mutations require you to authenticate using a JWT token.
You will first need to register as a user through the web app and then use your username and password to fetch a JWT token (accessToken in the payload below) as follows:

```
mutation {
   auth(password: "password", username: "johno") {
    __typename
    ... on AuthMutationSuccess {
      accessToken
      refreshToken
    }
    ... on AuthMutationFailed {
      reason
    }
   }
}
```

### Create a new post

To create a new post via the GraphQL API execute the following mutation in GraphiQL:

```
mutation {
  createPost (input: {
    token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNjE3NjQ3MjYzLCJuYmYiOjE2MTc2NDcyNjMsImp0aSI6IjMyODFiMGFhLTY3NGUtNDc2ZC04YTkzLWVmOTZiMjA0MTQyZiIsImlkZW50aXR5IjoiYXJub3V4IiwiZXhwIjoxNjE3NjQ4MTYzfQ.ruWw6GZxu4l2nnAC77Cf9MN7jLAiNbtcqjio9WD70Tc"
    title: "Test Post"
    content: "Test content"
  }) {
    __typename
    ... on CreatePostSuccess {
      post {
        id
        title
        content
        createdAt
        updatedAt
      }
    }
    ... on AuthInfoField {
      message
    }
  }
}
```
### Update a post

To update a post, execute the following mutation in GraphiQL:

```
mutation {
  updatePost(input: {
    token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNjE3NjQ3MjYzLCJuYmYiOjE2MTc2NDcyNjMsImp0aSI6IjMyODFiMGFhLTY3NGUtNDc2ZC04YTkzLWVmOTZiMjA0MTQyZiIsImlkZW50aXR5IjoiYXJub3V4IiwiZXhwIjoxNjE3NjQ4MTYzfQ.ruWw6GZxu4l2nnAC77Cf9MN7jLAiNbtcqjio9WD70Tc"
    id: "UG9zdE5vZGU6MTY="
    title: "Post apoca lyptic"
    content: "such content"
    tagNames: ["tech", "software"]
  }) {
    __typename
    ... on UpdatePostSuccess {
      post {
        id
        title
        content
        tagNames
      }
    }
    ... on UpdatePostFailed {
      reason
    }
    ... on AuthInfoField {
      message
		}
  }
}
```
Note that this method does not support patching a post record, so all fields must be sent across.

### Delete a post

To delete a post, execute the following mutation in GraphiQL:

```
mutation {
  deletePost(input: {
    token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNjE3NjQ3MjYzLCJuYmYiOjE2MTc2NDcyNjMsImp0aSI6IjMyODFiMGFhLTY3NGUtNDc2ZC04YTkzLWVmOTZiMjA0MTQyZiIsImlkZW50aXR5IjoiYXJub3V4IiwiZXhwIjoxNjE3NjQ4MTYzfQ.ruWw6GZxu4l2nnAC77Cf9MN7jLAiNbtcqjio9WD70Tc" 
    id: "UG9zdE5vZGU6MjI="
  }) {
    __typename
    ... on DeletePostSuccess {
      post {
        id
      }
    }
    ... on DeletePostFailed {
      reason
    }
    ... on AuthInfoField {
      message
    }
  }
}
```

## What you need to do

We need you to take this sample project, fork the repository, and add some extra features.

### Key goals and deliverables

- We would like to be able to tag posts by associating zero or more tags with a single post. (DONE)
- We would like to filter the list of posts by tag. (DONE)
- We would like to filter posts by the date they were created. (DONE)
- Some of our client consume the blog content via the GraphQL API. Currently they can only list and create posts, but have asked for the ability to edit and delete posts. (DONE)
- We would also like to filter posts by tag and creation date via the GraphQL API. (DONE)

**Bonus points**

- Implement user authentication (consider using [Flask-Login](https://flask-login.readthedocs.io/en/latest/)) (DONE)
- Deploy the project in AWS, Azure or GCP (DONE)
- Add unit tests for the new features (PARTIALLY DONE)

### Notes and observations from the dev

- The app has been deployed to an AWS EC2 instance and is available at: http://13.244.151.180:5000/
- The way that I have written the SQL query for filtering posts by creation date, and also the SQL query I wrote to expose the unique creation dates in the UI are very inefficient as I am using the SQL DATE function to cast the created_at datetime column to a date, resulting in the entire table needing to be scanned. I went on the assumption that the number of post records will stay small (at most a few thousand) and so performance would never be an issue. But if they were to grow to the tens of thousands or more, then we could optimise this by for example introducing a new table that stores only unique creation date values (using a unique index) and links back to the post through a joining table. We could then register an event handler on the posts model which would create and/or link the creation date table record to the post record automatically after the post record is created. Of course this is only one of many ways to solve this problem.
- I could not figure out how to turn my SQLAlchemy queries into reusable / chainable queries so they ended up living in the views where they are used. This is definitely not ideal as I feel that views should be for parsing params, passing them to methods that know how to run the business logic, and then serializing payloads. I found hybrid properties in the SQLAlchemy docs, and it looked promising, but then I realised it would not work for joins. With more time I would have worked on a solution that allows me to create a SQLAlchemy equivalent of Ruby on Rails' Active Record named scopes and then moved all these queries out of the views.
- I have not worked in Python for a few years now, and this was my first time to work with GraphQL. It was quite a learning experience! It was very tricky to find good examples online of what I wanted to achieve, and a lot of what I came across felt like hacky or incomplete solutions. I have definitely been spoilt by the Ruby and Rails communities.

### Dependencies and tools

You may install any other third-party dependencies and tools.

### Assignment submission

Submit this assignment by creating a fork of this repository in your own GitHub account and send a link to your _public_ fork to work@teamgeek.io (Please do not create a pull-request).

**NOTE:** Do not remove the *Plagiarism declaration*.

## Plagiarism declaration

1. I know that plagiarism is wrong. Plagiarism is to use another’s work and pretend that it is one’s own.
2. This assignment is my own work.
3. I have not allowed, and will not allow, anyone to copy my work with the intention of passing it off as his or her own work.
4. I acknowledge that copying someone else’s assignment (or part of it) is wrong and declare that my assignments are my own work.
