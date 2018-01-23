int main() {
    char S[100], c;
    fgets(S, 100, stdin);
    scanf("%c", &c);
    for (int i = 0; i < strlen(S); i++) {
        if(S[i] == c) { 
            S[i] = '\0';
            break;
        }
    }
    puts(S);
}