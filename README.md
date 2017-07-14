# tf-vardoc


## Important Note
This is a _work-in-progress_!  It still needs to be "productionalized" by making it into a proper commandline utility.

## What is this?
This is a utility for generating documentation regarding [Terraform](https://github.com/hashicorp/terraform)
variables.

## Why is that important?
1. The only thing worse than _no documentation_ is _stale/incorrect documentation_.
2. A part of defining Terraform variables is self-documentatin; you set variable types, descriptions, and defaults as code.
3. While you could just _read the code_, it's good practice to include a `README.md` for any Terraform module.
4. This is now a problem if you like to make purdy, stylized `README`s; there's no easy/quick way to transform your
   variable definitions to documentation.

*Until now...*

## How do I use it?
Create a `README.md.j2` [jinja2 template](http://jinja.pocoo.org/docs/2.9/). Your variables will be available under
the `variables` variable.  Stylize to your hearts content.

## TODO
- make this a proper commandline tool with args and configuration
- setup pip package
- distribute
