# CDNDetect
A python service that will detect the CDNs used by a website.

The cdn.json file was originally sourced from 
https://github.com/turbobytes/cdnfinder/blob/master/assets/cnamechain.json.
A few small additions have been made, and PRed back to the cdnfinder project.

### Issues encountered
* If assets are hosted on a different domain, should this be detected? E.g. tweakers.net using assets from
the tweakers.nl domain.
* During development I am having some issues with DNS - records that certainly exist won't be resolved,
  eg: `dns.resolver.NoAnswer: The DNS response does not contain an answer to the question: funnygames.at. IN A`
  This makes testing problematic.