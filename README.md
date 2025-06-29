# Can I park?

Driving to Ghent and want to know if there is place in one of the car parks
managed by the city, without leaving the warmth of your terminal before you
leave? Look no further than this utility!

## How to install

### Using pip

```
pip install can-i-park
```

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
