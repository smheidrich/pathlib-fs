# Notes on testing

## Types of tests

### Original idea I had for categorization

- Common (OSFS + MemoryFS + ...)
    - modify something on FS using our library, check with PyFilesystem that it
      worked
    - modify something on FS using PyFilesystem, check with our library that
      state is represented correctly
    - => **"tests against PyFilesystem"**
    - additionally: **self-consistency** tests: modify using our library, check
      with our library that it worked
        - these could actually be provided as a kind of "library of tests" that
          anyone re-implementing the pathlib interface could use! because it's
          the same for each pathlib interface implementation
- only OSFS
    - modify something on FS using our library, check with pathlib that it
      worked
    - modify something on FS using pathlib, check with our library that state
      is represented correctly
    - => **"tests against pathlib"**

#### New idea

- Methods that modify filesystem state (open(w), mkdir, ...)
    - modify something on FS using our library
        - any FS: check with PyFilesystem that it worked
        - OSFS: check with pathlib that it worked
        - **self-consistency**: check with our library that it worked
            - these could actually be provided as a kind of "library of tests"
              that anyone re-implementing the pathlib interface could use!
              because it's the same for each pathlib interface implementation
- Methods that check filesystem state (exists, is_dir, ...)
    - any FS: modify something on FS with PyFilesystem
    - OSFS: modify something on FS with pathlib
    - in both cases: check with our library that it worked
