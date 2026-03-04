// minify.c - custom code formatter 
// this tool has primarily been designed for LastRedux
// 
// if you don't know what this does,
// you probably shouldn't be using it
//
// https://github.com/LastRedux/LastRedux

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

typedef struct {
	char* data;
	size_t len;
	size_t cap;
} buf;

static void bufInit(buf* b){
	b->cap = 4096;
	b->data = (char*)malloc(b->cap);
	b->len = 0;
}

static void bufPush(buf* b,char c){
	if(b->len >= b->cap){
		b->cap *= 2;
		b->data = (char*)realloc(b->data,b->cap);
	}
	b->data[b->len++] = c;
}

static void bufFree(buf* b){
	free(b->data);
}

static char* readFile(const char* path,size_t* out_len){
	FILE* f = fopen(path,"rb");
	if(!f) return NULL;
	
	fseek(f,0,SEEK_END);
	size_t len = ftell(f);
	fseek(f,0,SEEK_SET);

	//explicit cast to shut the LSP up
	char* data = (char*)malloc(len + 1);
	
	fread(data,1,len,f);
	data[len] = '\0';
	fclose(f);

	*out_len = len;
	return data;
}

static bool writeFile(const char* path,const char* data,size_t len){
	FILE* f = fopen(path,"wb");
	if(!f) return false;
	fwrite(data,1,len,f);
	fclose(f);
	return true;
}

static bool endsWith(const char* str,const char* suffix){
	size_t slen = strlen(str);
	size_t suflen = strlen(suffix);
	if(suflen > slen) return false;
	return strcmp(str + slen - suflen,suffix) == 0;
}

static bool isIndent(char c){
	return isalnum((unsigned char)c) || c == '_';
}

static bool isLabelSkippable(const char* src, size_t pos){
			if(pos < 4) return false;
			size_t i = pos - 1;
			while(i > 0 && src[i] == ' ') i--;
			size_t end = i;
			while(i > 0 && isIndent(src[i-1])) i--;
			const char* word = src + i;
			switch(end - i + 1){
				case 4: return memcmp(word, "case", 4) == 0;
				case 5: return memcmp(word, "slots", 5) == 0;
				case 6: return memcmp(word, "public", 6) == 0;
				case 7: return memcmp(word, "default", 7) == 0 ||
								memcmp(word, "private", 7) == 0 ||
								memcmp(word, "signals", 7) == 0;
				case 9: return memcmp(word, "protected", 9) == 0;
				default: return false;
			}
}

static bool isColonInLoop(const char* src,size_t pos){
	int depth = 0;
	for(size_t i = pos; i > 0; i--){
		if(src[i] == ')') depth++;
		else if(src[i] == '(') {
			depth--;
			if(depth < 0){
				size_t j = i - 1;
				while(j > 0 && (src[j] == ' ' || src[j] == '\t')) j--;
				if(j >= 2 && strncmp(src+j-2,"for",3) == 0) return true;
				return false;
			}
		}
	}
	return false;
}

static bool isDeclaration(const char* src,size_t pos){
	int depth = 0;
	int bDepth = 0;
	size_t lineStrt = pos;
	while(lineStrt > 0 && src[lineStrt-1] != '\n') lineStrt--;
	for(size_t i = lineStrt; i < pos; i++){
		if(src[i] == '(') depth++;
		else if(src[i] == ')') depth--;
		else if(src[i] == '[') bDepth++;
		else if(src[i] == ']') bDepth--;
	}
	if(depth > 0) return true;
	if(bDepth == 0){
		for(size_t i = lineStrt; i < pos; i++){
			if(src[i] == '[') return false;
		}
	} else return false;
	size_t i = lineStrt;
	while(src[i] == ' ' || src[i] == '\t') i++;
	int ident_count = 0;
	bool in_ident = false;
	for(size_t j = i; j < pos; j++){
		if(isIndent(src[j])){
			if(!in_ident){ in_ident = true; ident_count++; }
		} else in_ident = false;
	}
	if(ident_count >= 2){
		for(size_t j = pos; src[j] && src[j] != '\n'; j++){
			if(src[j] == ';') return true;
			if(src[j] == '{') return false;
		}
	}
	return false;
}

static void minifyCpp(const char* src,size_t len,buf* out){
	for(size_t i = 0; i < len; i++){
		char c = src[i];
		char next = (i+1 < len) ? src[i+1] : '\0';
		char prev = (i > 0) ? src[i-1] : '\0';

		if(c == ' ' && next == '{' && (prev == ')' || isIndent(prev))){
			continue;
		}

		if(c == ',' && next == ' '){
			bufPush(out,c);
			i++;
			continue;
		}

		if(c == ' ' && next == ':' && i+1 < len){
			if(!isLabelSkippable(src,i+1) && !isColonInLoop(src,i+1)){
				size_t j = i+2;
				while(j < len && src[j] == ' ') j++;
				if(j < len && isIndent(src[j]) && (isIndent(prev) || prev == ')')){
					continue; // Skip space before :
				}
			}
		}
		if(c == ':' && next == ' '){
			if(!isLabelSkippable(src,i) && !isColonInLoop(src,i)){
				size_t j = i+2;
				while(j < len && src[j] == ' ') j++;
				size_t k = i-1;
				while(k > 0 && src[k] == ' ') k--;
				if(j < len && isIndent(src[j]) && k > 0 && (isIndent(src[k]) || src[k] == ')')){
					bufPush(out,c);
					i++;
					continue;
				}
			}
		}

		if(c == ' ' && next == '=' && i+2 < len && src[i+2] != '=' && isDeclaration(src,i+1)){
			continue;
		}
		if(c == '=' && next == ' ' && isDeclaration(src,i)){
			if(prev == '!' || prev == '=' || prev == '<' || prev == '>' ||
			   prev == '+' || prev == '-' || prev == '*' || prev == '/' ||
			   prev == '%' || prev == '&' || prev == '|' || prev == '^'){
				bufPush(out,c);
				continue;
			}
			bufPush(out,c);
			i++;
			continue;
		}

		bufPush(out,c);
	}
}

static void minifyQml(const char* src,size_t len,buf* out){
	for(size_t i = 0; i < len; i++){
		char c = src[i];
		char next = (i+1 < len) ? src[i+1] : '\0';
		char prev = (i > 0) ? src[i-1] : '\0';

		if(c == ' ' && next == '{' && isIndent(prev)){
			continue;
		}

		if(c == ' ' && next == ':'){
			continue;
		}
		if(c == ':' && next == ' '){
			bufPush(out,c);
			i++;
			continue;
		}

		bufPush(out,c);
	}
}

int main(int argc,char* argv[]){
	static const char* str = "usage: minify [-w] <file>\n";
	bool w = false;
	const char* path = NULL;

	for(int i = 1; i < argc; i++){
		if(strcmp(argv[i],"-w") == 0) w = true;
		else if(strcmp(argv[i],"-h") == 0 || strcmp(argv[i],"--help") == 0){
			printf("%s",str);
			printf("  -w: write changes immediately without preview\n");
			printf("  applies \"minified\" code style to C++/QML files\n");
			return 0;
		}
		else path = argv[i];
	}

	if(!path){
		fprintf(stderr,"%s",str);
		return 1;
	}

	size_t srcLen;
	char* src = readFile(path,&srcLen);
	if(!src){
		fprintf(stderr,"error: cannot read %s\n",path);
		return 1;
	}

	bool isQml = endsWith(path,".qml");
	buf out;
	bufInit(&out);

	if(isQml) minifyQml(src,srcLen,&out);
	else minifyCpp(src,srcLen,&out);

	fprintf(stdout,"attempting to process %s...\n", path);

	if(w){
		if(!writeFile(path,out.data,out.len)){
			fprintf(stderr,"error: cannot write %s\n",path);
			bufFree(&out);
			free(src);
			return 1;
		}
	} else {
		fwrite(out.data,1,out.len,stdout);
	}

	bufFree(&out);
	free(src);
	fprintf(stdout,"done\n");
	return 0;
}
