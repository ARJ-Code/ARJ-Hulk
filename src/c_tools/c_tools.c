#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define bool int

typedef struct Entry
{
    char *key;
    void *value;
    struct Entry *next;
} Entry;

typedef struct Type
{
    Entry *head;
} Type;

// Type

Type *system_eqType(Type *t1, Type *t2);
Type *system_toStringType(Type *t);

// String

Type *system_createString(char *value);
Type *system_lengthString(Type *string);
Type *system_getString(Type *string, Type *index);
Type *system_eqString(Type *string1, Type *string2);
Type *system_compString(Type *string1, Type *string2);
Type *system_currentString(Type *list);
Type *system_nextString(Type *list);
Type *system_resetString(Type *list);
Type *system_concatString(Type *string1, Type *string2);
Type *system_concatWithSpaceString(Type *string1, Type *string2);
Type *system_subString(Type *string, Type *start, Type *end);
Type *system_toStringString(Type *string);

// Number

Type *system_createNumber(double n);
Type *system_eqNumber(Type *n1, Type *n2);
Type *system_compNumber(Type *n1, Type *n2);
Type *system_addNumber(Type *n1, Type *n2);
Type *system_subNumber(Type *n1, Type *n2);
Type *system_mulNumber(Type *n1, Type *n2);
Type *system_divNumber(Type *n1, Type *n2);
Type *system_powNumber(Type *n1, Type *n2);
Type *system_toStringNumber(Type *n);

// Boolean

Type *system_createBoolean(bool n);
Type *system_eqBoolean(Type *n1, Type *n2);
Type *system_toStringBoolean(Type *n);
Type *system_andBoolean(Type *n1, Type *n2);
Type *system_orBoolean(Type *n1, Type *n2);
Type *system_notBoolean(Type *n);

// List Type

Type *system_createList();
Type *system_lengthList(Type *list);
Type *system_addList(Type *list, Type *item);
Type *system_getList(Type *list, Type *index);
Type *system_setList(Type *list, Type *index, Type *item);
Type *system_containsList(Type *list, Type *item);
Type *system_removedList(Type *list, Type *index);
Type *system_currentList(Type *list);
Type *system_nextList(Type *list);
Type *system_resetList(Type *list);
Type *system_toStringList(Type *list);

// Aux functions

double system_typeToDouble(Type *t);
bool system_typeToBoolean(Type *t);
Type *system_copyNumber(Type *t);
Type *system_copyBoolean(Type *t);
Type *system_eq(Type *t1, Type *t2);
Type *system_comp(Type *t1, Type *t2);

// Type

Type *system_createType()
{
    Type *dict = malloc(sizeof(Type));
    dict->head = NULL;
    return dict;
}

void system_addEntry(Type *dict, char *key, void *value)
{
    Entry *newEntry = malloc(sizeof(Entry));
    newEntry->key = strdup(key);
    newEntry->value = value;
    newEntry->next = dict->head;
    dict->head = newEntry;
}

void *system_findEntry(Type *dict, char *key)
{
    Entry *current = dict->head;
    while (current != NULL)
    {
        if (strcmp(current->key, key) == 0)
        {
            return current->value;
        }
        current = current->next;
    }
    return NULL;
}

void system_removeEntry(Type *dict, char *key)
{
    Entry *current = dict->head;
    Entry *prev = NULL;
    while (current != NULL)
    {
        if (strcmp(current->key, key) == 0)
        {
            if (prev == NULL)
            {
                dict->head = current->next;
            }
            else
            {
                prev->next = current->next;
            }
            free(current->key);
            free(current);
            return;
        }
        prev = current;
        current = current->next;
    }
}

void system_freeType(Type *dict)
{
    Entry *current = dict->head;
    while (current != NULL)
    {
        Entry *next = current->next;
        free(current->key);
        free(current);
        current = next;
    }
    free(dict);
}

Type *system_eqType(Type *t1, Type *t2)
{
    return system_createBoolean(t1 == t2);
}

Type *system_toStringType(Type *t)
{
    char *type = system_findEntry(t, "type");

    return system_createString(type);
}

// String

Type *system_createString(char *value)
{
    Type *s = system_createType();
    int *len = malloc(sizeof(int));
    int *curr = malloc(sizeof(int));

    char *s_value = malloc(sizeof(strlen(value)));
    strcpy(s_value, value);

    *len = strlen(value);
    *curr = 0;

    system_addEntry(s, "type", "String");
    system_addEntry(s, "value", s_value);
    system_addEntry(s, "len", len);
    system_addEntry(s, "curr", curr);

    system_addEntry(s, "length", *system_lengthString);

    system_addEntry(s, "get", *system_getString);

    system_addEntry(s, "comp", *system_compString);

    system_addEntry(s, "current", *system_currentString);
    system_addEntry(s, "next", *system_nextString);
    system_addEntry(s, "reset", *system_resetString);

    system_addEntry(s, "subString", *system_subString);

    system_addEntry(s, "eq", *system_eqString);
    system_addEntry(s, "toString", *system_toStringString);

    return s;
}

Type *system_lengthString(Type *string)
{
    int *len = system_findEntry(string, "len");

    return system_createNumber(*len);
}

Type *system_getString(Type *string, Type *p_index)
{
    int index = system_typeToDouble(p_index);
    char *aux = malloc(sizeof(char));
    char *value = system_findEntry(string, "value");
    aux[0] = value[index];
    aux[1] = '\0';
    Type *q = system_createString(aux);

    free(aux);

    return q;
}

Type *system_eqString(Type *string1, Type *string2)
{
    char *value1 = system_findEntry(string1, "value");
    char *value2 = system_findEntry(string2, "value");

    return system_createBoolean(strcmp(value1, value2) == 0);
}

Type *system_compString(Type *string1, Type *string2)
{
    char *value1 = system_findEntry(string1, "value");
    char *value2 = system_findEntry(string2, "value");

    int r = strcmp(value1, value2);
    if (r < 1)
        return system_createNumber(-1);
    if (r == 0)
        return system_createNumber(0);
    return system_createNumber(1);
}

Type *system_currentString(Type *list)
{
    int *curr = (int *)system_findEntry(list, "curr");

    Type *aux = system_createNumber(*curr);
    Type *res = system_getString(list, aux);
    free(aux);
    return res;
}

Type *system_nextString(Type *list)
{
    int *curr = (int *)system_findEntry(list, "curr");
    int *len = (int *)system_findEntry(list, "len");

    if (*curr == *len)
        return system_createBoolean(0);

    *curr = *curr + 1;

    return system_createBoolean(1);
}

Type *system_resetString(Type *list)
{
    int *curr = (int *)system_findEntry(list, "curr");
    *curr = 0;

    return list;
}

Type *system_concatString(Type *string1, Type *string2)
{
    Type *(*toString1)(Type *) = system_findEntry(string1, "toString");
    Type *(*toString2)(Type *) = system_findEntry(string2, "toString");

    string1 = toString1(string1);
    string2 = toString2(string2);

    int *len1 = system_findEntry(string1, "len");
    int *len2 = system_findEntry(string2, "len");

    char *value1 = system_findEntry(string1, "value");
    char *value2 = system_findEntry(string2, "value");

    char *aux = malloc(sizeof(char) * (*len1 + *len2 + 1));
    strcpy(aux, value1);
    strcat(aux, value2);
    return system_createString(aux);
}

Type *system_concatWithSpaceString(Type *string1, Type *string2)
{
    Type *(*toString1)(Type *) = system_findEntry(string1, "toString");
    Type *(*toString2)(Type *) = system_findEntry(string2, "toString");

    string1 = toString1(string1);
    string2 = toString2(string2);

    int *len1 = system_findEntry(string1, "len");
    int *len2 = system_findEntry(string2, "len");

    char *value1 = system_findEntry(string1, "value");
    char *value2 = system_findEntry(string2, "value");

    char *aux = malloc(sizeof(char) * (*len1 + *len2 + 2));
    strcpy(aux, value1);
    strcat(aux, " ");
    strcat(aux, value2);
    return system_createString(aux);
}

Type *system_subString(Type *string, Type *p_start, Type *p_end)
{
    int start = system_typeToDouble(p_start);
    int end = system_typeToDouble(p_end);

    char *aux = malloc(sizeof(char) * (end - start + 1));
    char *value = system_findEntry(string, "value");

    for (int i = start; i < end; i++)
    {
        aux[i - start] = value[i];
    }
    aux[end - start] = '\0';
    return system_createString(aux);
}

Type *system_toStringString(Type *string)
{
    return string;
}

// Number

Type *system_createNumber(double n)
{
    Type *t = system_createType();

    double *value = malloc(sizeof(int));
    *value = n;

    system_addEntry(t, "type", "Number");
    system_addEntry(t, "value", value);

    system_addEntry(t, "comp", *system_compNumber);

    system_addEntry(t, "eq", *system_eqNumber);
    system_addEntry(t, "toString", *system_toStringNumber);
}

Type *system_parseNumber(Type *string)
{
    char *value = system_findEntry(string, "value");

    return system_createNumber(strtod(value, NULL));
}

Type *system_eqNumber(Type *n1, Type *n2)
{
    return system_createBoolean(system_typeToDouble(n1) == system_typeToDouble(n2));
}

Type *system_compNumber(Type *n1, Type *n2)
{
    double nn1 = system_typeToDouble(n1);
    double nn2 = system_typeToDouble(n2);

    if (nn1 > nn2)
        return system_createNumber(1);
    if (nn1 == nn2)
        return system_createNumber(0);

    return system_createNumber(-1);
}

Type *system_toStringNumber(Type *n)
{
    double *value = system_findEntry(n, "value");

    char str[1024];
    sprintf(str, "%f", *value);
    return system_createString(str);
}

double system_typeToDouble(Type *t)
{
    double *value = system_findEntry(t, "value");
    return *value;
}

Type *system_copyNumber(Type *t)
{
    return system_createNumber(system_typeToDouble(t));
}

Type *system_addNumber(Type *n1, Type *n2)
{
    double nn1 = system_typeToDouble(n1);
    double nn2 = system_typeToDouble(n2);

    return system_createNumber(nn1 + nn2);
}

Type *system_subNumber(Type *n1, Type *n2)
{
    double nn1 = system_typeToDouble(n1);
    double nn2 = system_typeToDouble(n2);

    return system_createNumber(nn1 - nn2);
}
Type *system_mulNumber(Type *n1, Type *n2)
{
    double nn1 = system_typeToDouble(n1);
    double nn2 = system_typeToDouble(n2);

    return system_createNumber(nn1 * nn2);
}

Type *system_divNumber(Type *n1, Type *n2)
{
    double nn1 = system_typeToDouble(n1);
    double nn2 = system_typeToDouble(n2);

    return system_createNumber(nn1 / nn2);
}

Type *system_powNumber(Type *n1, Type *n2)
{
    double nn1 = system_typeToDouble(n1);
    double nn2 = system_typeToDouble(n2);

    double pow = 1;

    for (int i = 0; i < nn2; i++)
        pow *= nn1;

    return system_createNumber(pow);
}

// Boolean

Type *system_createBoolean(bool n)
{
    Type *t = system_createType();
    bool *value = malloc(sizeof(int));
    *value = n;

    system_addEntry(t, "type", "Boolean");
    system_addEntry(t, "value", value);

    system_addEntry(t, "eq", *system_eqBoolean);
    system_addEntry(t, "toString", *system_toStringBoolean);
}

Type *system_eqBoolean(Type *n1, Type *n2)
{
    return system_createBoolean(system_typeToBoolean(n1) == system_typeToBoolean(n2));
}

Type *system_toStringBoolean(Type *n)
{
    bool nn = system_typeToBoolean(n);
    if (nn == 1)
        return system_createString("true");
    return system_createString("false");
}

bool system_typeToBoolean(Type *t)
{
    bool *value = system_findEntry(t, "value");
    return *value;
}

Type *system_copyBoolean(Type *t)
{
    return system_createBoolean(system_typeToBoolean(t));
}

Type *system_andBoolean(Type *n1, Type *n2)
{
    return system_createBoolean(system_typeToBoolean(n1) && system_typeToBoolean(n2));
}

Type *system_orBoolean(Type *n1, Type *n2)
{
    return system_createBoolean(system_typeToBoolean(n1) || system_typeToBoolean(n2));
}
Type *system_notBoolean(Type *n)
{
    return system_createBoolean(!system_typeToBoolean(n));
}

// List

Type *system_createList()
{
    Type *l = system_createType();
    Type **array = malloc(sizeof(Type *) * 32);

    int *cap = malloc(sizeof(int));
    int *len = malloc(sizeof(int));
    int *curr = malloc(sizeof(int));
    *cap = 32;
    *len = 0;
    *curr = 0;

    system_addEntry(l, "type", "List");

    system_addEntry(l, "array", array);
    system_addEntry(l, "capacity", cap);
    system_addEntry(l, "len", len);
    system_addEntry(l, "curr", curr);

    system_addEntry(l, "length", *system_lengthList);
    system_addEntry(l, "add", *system_addList);
    system_addEntry(l, "contains", *system_containsList);
    system_addEntry(l, "removed", *system_removedList);

    system_addEntry(l, "get", *system_getList);

    system_addEntry(l, "set", *system_setList);

    system_addEntry(l, "current", *system_currentList);
    system_addEntry(l, "next", *system_nextList);
    system_addEntry(l, "reset", *system_resetList);

    system_addEntry(l, "eq", *system_eqType);
    system_addEntry(l, "toString", *system_toStringList);

    return l;
}

Type *system_lengthList(Type *list)
{
    int *len = system_findEntry(list, "len");

    return system_createNumber(*len);
}

Type *system_addList(Type *list, Type *item)
{
    int *len = (int *)system_findEntry(list, "len");
    int *capacity = (int *)system_findEntry(list, "capacity");
    Type **array = (Type **)system_findEntry(list, "array");

    if (*len == *capacity)
    {
        *capacity = *capacity * 2;
        array = realloc(array, *capacity * sizeof(Type *));
    }

    array[*len] = item;
    *len = *len + 1;

    return item;
}

Type *system_getList(Type *list, Type *p_index)
{
    int index = system_typeToDouble(p_index);
    Type **array = (Type **)system_findEntry(list, "array");
    return array[index];
}

Type *system_setList(Type *list, Type *p_index, Type *item)
{
    int index = system_typeToDouble(p_index);
    Type **array = (Type **)system_findEntry(list, "array");
    array[index] = item;

    return item;
}

Type *system_containsList(Type *list, Type *item)
{
    return system_createBoolean(0);
}

Type *system_removedList(Type *list, Type *p_index)
{
    int index = system_typeToDouble(p_index);

    int *len = (int *)system_findEntry(list, "len");
    Type **array = (Type **)system_findEntry(list, "array");

    Type *item = array[index];

    for (int i = index; i < *len - 1; i++)
    {
        array[i] = array[i + 1];
    }
    *len = *len - 1;

    return item;
}

Type *system_currentList(Type *list)
{
    int *curr = (int *)system_findEntry(list, "curr");

    Type *aux = system_createNumber(*curr);
    Type *res = system_getString(list, aux);
    free(aux);
    return res;
}

Type *system_nextList(Type *list)
{
    int *curr = (int *)system_findEntry(list, "curr");
    int *len = (int *)system_findEntry(list, "len");

    if (*curr == *len)
        return system_createBoolean(0);

    *curr = *curr + 1;

    return system_createBoolean(1);
}

Type *system_resetList(Type *list)
{
    int *curr = (int *)system_findEntry(list, "curr");
    *curr = 0;

    return list;
}

Type *system_toStringList(Type *list)
{
    int *len = (int *)system_findEntry(list, "len");
    Type **array = (Type **)system_findEntry(list, "array");

    Type *s = system_createString("[");

    for (int i = 0; i < *len; i++)
    {
        Type *aux = system_concatString(s, array[i]);
        free(s);
        s = aux;

        if (i != *len - 1)
        {
            aux = system_concatString(s, system_createString(","));
            free(s);
            s = aux;
        }
    }

    Type *q = system_createString("]");
    Type *aux = system_concatString(s, q);

    free(s);
    free(q);

    s = aux;
}

Type *system_eq(Type *t1, Type *t2)
{
    Type *(*eq)(Type *, Type *) = system_findEntry(t1, "eq");

    return eq(t1, t2);
}

Type *system_comp(Type *t1, Type *t2)
{
    Type *(*comp)(Type *, Type *) = system_findEntry(t1, "comp");

    return comp(t1, t2);
}

Type *system_print(Type *t)
{
    Type *(*toString)(Type *) = system_findEntry(t, "toString");
    Type *s = toString(t);

    char *value = system_findEntry(s, "value");
    printf("%s\n", value);

    return t;
}

// FINISH C TOOLS

int main()
{
    Type *a = system_createNumber(0);
    Type *l = system_createList(1);
    Type *l1 = system_createList(1);

    system_addList(l, a);
    system_addList(l1, a);

    system_addList(l, system_createBoolean(0));

    system_print(system_getList(l, a));

    return 0;
}
