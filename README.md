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

- We would like to be able to tag posts by associating zero or more tags with a single post.
- We would like to filter the list of posts by tag.
- We would like to filter posts by the date they were created.
- Some of our client consume the blog content via the GraphQL API. Currently they can only list and create posts, but have asked for the ability to edit and delete posts.
- We would also like to filter posts by tag and creation date via the GraphQL API.

**Bonus points**

- Implement user authentication (consider using [Flask-Login](https://flask-login.readthedocs.io/en/latest/))
- Deploy the project in AWS, Azure or GCP
- Add unit tests for the new features

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
