# CDNDetect
A python service that will detect the CDNs used by a website


### Issues encountered
* If assets are hosted on a different domain, should this be detected?
* During development I am having some issues with DNS - records that certainly exist won't be resolved,
  eg: `dns.resolver.NoAnswer: The DNS response does not contain an answer to the question: funnygames.at. IN A`
  This makes testing problematic.