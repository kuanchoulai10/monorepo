---
tags:
  - JWT
  - Security
---

# JSON Web Tokens (JWT)

<iframe width="560" height="315" src="https://www.youtube.com/embed/P2CPd9ynFLg?si=0GU2AXKssHjcTKbf" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
/// caption
[Why is JWT popular?](https://www.youtube.com/watch?v=P2CPd9ynFLg)
///


![](https://cdn.sanity.io/images/3jwyzebk/production/c098fa07deca1062e013d92cabba4ba7ec7e7f19-1584x988.png?auto=format&fit=max&w=3840&q=75)
/// caption
[Structure of a JSON web token](https://stytch.com/blog/what-is-a-json-web-token/)
///

<iframe width="560" height="315" src="https://www.youtube.com/embed/0WH9oiYMS3M?si=lv69Rj6QvfttcPD4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
/// caption
[JWT - JSON Web Token explained in 4 minutes (With Visuals)](https://www.youtube.com/watch?v=0WH9oiYMS3M)
///

## Header

## Payload

Common claim types:

- `iss` (Issuer): Identifies who issued the token.
- `sub` (Subject): Represents the user or entity the token is about.
- `aud` (Audience): Specifies the intended recipient.
- `exp` (Expiration): Defines when the token expires.
- `iat` (Issued At): Timestamp when the token was created.
- `nbf` (Not Before): Specifies when the token becomes valid.

## Signature

The signature is created by **taking the encoded header, the encoded payload, a secret key, and the algorithm specified in the header**. The signature **ensures that the token hasn't been altered**.

## References

- [Components of JWTs Explained](https://fusionauth.io/articles/tokens/jwt-components-explained)
