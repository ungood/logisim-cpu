ifeq ($(VIRTUAL_ENV),)
  $(error VIRTUAL_ENV is not set! Did you forget to activate it?)
endif

.PHONY: clean

compiler_dir  := ./compiler
diagram_dir   := ./diagrams
microcode_dir := ./microcode
programs_dir  := ./programs

compiler := $(VIRTUAL_ENV)/bin/sappy

assembly_files := $(wildcard $(programs_dir)/*.asm)
object_files := $(patsubst %.asm,%.o,$(subst $(programs_dir),$(programs_dir),$(assembly_files)))
binary_files := $(patsubst %.asm,%.raw,$(subst $(programs_dir),$(programs_dir),$(assembly_files)))
compilers := $(wildcard $(compiler_dir)/*.py)

all: microcode diagrams binaries

$(compiler): $(compilers)
	@ echo "Installing the 'sappy' compiler."
	pip install -e compiler

microcode: $(microcode_dir)/SAP-1.raw $(microcode_dir)/SAP-1b.raw

$(microcode_dir)/%.raw: $(compiler)
	@ echo "\nWriting microcode for $*:"
	$(compiler) write-microcode --arch $* $@

diagrams: $(diagram_dir)/object-code.html $(diagram_dir)/assembly.html

$(diagram_dir)/object-code.html: $(compilers)
	@ echo "\nWriting object code diagram to $@:"
	$(compiler) write-object-code-diagram $@

$(diagram_dir)/assembly.html: $(compilers)
	@ echo "\nWriting assembly diagram to $@:"
	$(compiler) write-assembly-diagram $@

binaries: $(binary_files)

$(programs_dir)/%.raw: $(programs_dir)/%.o $(compilers)
	@ echo "\nLinking $< to $@:"
	$(compiler) link $< $@

objects: $(object_files)

$(programs_dir)/%.o: $(programs_dir)/%.asm $(compilers)
	@ echo "\nAssembling $< to $@:"
	$(compiler) assemble $< $@