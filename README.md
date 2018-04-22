Hadrian's Wall
====

![](wall.jpg)

Nightly integration test system and status site for
[the new GHC build system Hadrian based on Shake build](https://github.com/snowleopard/hadrian).

---

Here is the motivation: https://github.com/snowleopard/hadrian/issues/348

We will be mainly using this site as a post-merge stat tracker.
So we need to extract and maintain data from daily builds & tests output
([Hadrian's brick](https://github.com/monad-systems/hadrians-brick)),
analyze them in this backend, and let python server to retrieve build's metadata
and display nicely in front-end.

## Contributions are highly appreciated!

See https://github.com/izgzhen/hadrians-brick.
