# Actionable steps to write or organize code cleanly

# code design
1. seperate logic:
      by service (business capability, externally visible).
      by layer (technical capability, only internally visible).
3. Identify class and main methods: using SVO strategy to satisfy single responsibility principle and make sure the number of method parameters doesn't exceed three.
4. Only use inheritance when we can make sure it's relationship will never change (prioritize composition over inheritance).

# code implement (using llm)
4. Write unit test for main methods
5. Coding

# review (support by llm)
6. Make sure function not too lengthy.
7. Remove duplicated code segments.


