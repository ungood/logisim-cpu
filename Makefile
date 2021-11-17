.PHONY: clean

source_dir := ./assembly
output_dir := ./binaries
compiler_dir := ./compiler

sources := $(wildcard $(source_dir)/*.asm)
output := $(patsubst %.asm,%.raw,$(subst $(source_dir),$(output_dir),$(sources)))
compilers := $(wildcard $(compiler_dir)/*.py)

all: microcode.raw $(output)

microcode.raw: $(compilers)
	$(compiler_dir)/create_microcode.py > microcode.raw

$(output_dir)/%.raw: $(source_dir)/%.asm $(compilers)
	$(info Assembling $< to $@\n)
	$(compiler_dir)/assembler.py $< > $@
#	@ mkdir -p $(abspath $(dir $@))
#	@ j2 $< > $@
