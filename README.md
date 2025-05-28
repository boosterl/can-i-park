# Can I park?

It's a question you might have asked yourself before if you have a BEV/PHEV.
This utility allows you to check if your favorite charging stations are available
for your car to charge, right from the warmth of your terminal! No need to go
outside and physically check if the charging station is available, and possibly
return disappointed because it was occupied.

## How to use

### CLI

The CLI can be used in the following ways:

```bash
# Using arguments
$ can-i-park
# Arguments can be passed to filter on garages, if they are in a low emission zone and for showing extra information about the garage
$ can-i-park --name sint-pieters --no-lez -v
# The script can also be called using it's abbreviation
$ cip
```

## See it in action

![GIF of an example session interacting with the cli](demo.gif)
