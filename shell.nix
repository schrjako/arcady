{ pkgs ? import <nixpkgs> {} }:
	pkgs.mkShell {
		nativeBuildInputs = with pkgs; [
			python312
			python312Packages.pygame
		];
		shellHook = ''
		'';
}
