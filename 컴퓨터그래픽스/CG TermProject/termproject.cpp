#include <GL/glew.h> // �ʿ��� ������� include 
#include <GL/freeglut.h> 
#include <GL/freeglut_ext.h>
#include "glm/glm/glm.hpp"
#include "glm/glm/ext.hpp"
#include "glm/glm/gtc/matrix_transform.hpp"
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <random>
#include <cmath>
#include <time.h>
#include <vector>
#include <iterator>

#define STB_IMAGE_IMPLEMENTATION
#include "���.h"

using namespace std;

char* filetobuf(const char *file) {
	FILE *fptr;
	long length;
	char *buf;
	fptr = fopen(file, "rb"); // Open file for reading 
	if (!fptr) // Return NULL on failure 
		return NULL;
	fseek(fptr, 0, SEEK_END); // Seek to the end of the file 
	length = ftell(fptr); // Find out how many bytes into the file we are 
	buf = (char*)malloc(length + 1); // Allocate a buffer for the entire length of the file and a null terminator 
	fseek(fptr, 0, SEEK_SET); // Go back to the beginning of the file 
	fread(buf, length, 1, fptr); // Read the contents of the file in to the buffer 
	fclose(fptr); // Close the file 
	buf[length] = 0; // Null terminator 
	return buf; // Return the buffer 
}

int life = 10;
int t = 0;
int dt = 1; //�ð��� �����ϴ� ��

float dis_l = 0;
float dis_r = 0;


float dis_oc_lr = 0;
float dis_oc_rl = 0;



int testnum = 0;

float obs_bb_x = 0.15f;
float body_bb_x = 0;
//GLboolean is_collide = false;

random_device rng;

uniform_real_distribution<float>uid(-0.5f, 0.5f);

uniform_real_distribution<float>uid_t(-100.f, -30.0f);

//snow
uniform_real_distribution<float>uid_snow_x(-0.5f, 0.5f);
uniform_real_distribution<float>uid_snow_y(0.8f, 1.0f);
uniform_real_distribution<float>uid_snow_z(-100.f, 100.0f);

//ring_obs
uniform_real_distribution<float>uid_ring(-0.25f, 0.25f);



default_random_engine dre(rng());

uniform_int_distribution<>uid2(0, 2);
default_random_engine dre2(rng());




GLvoid drawScene(GLvoid);
GLvoid Reshape(int w, int h);
GLuint cube_vao[1], cube_vbo[1], cube_ebo[1], light_vao, light_vbo;
GLuint game_over_vao, game_over_vbo, game_over_ebo;
GLuint ground_vao, ground_vbo;
GLuint obs_vao[3], obs_vbo[3];
GLuint tree_vao[1], tree_vbo[1];
GLchar *vertexsource, *fragmentsource; // �ҽ��ڵ����庯��
GLuint vertexshader, fragmentshader; // ���̴�
GLuint shaderprogram; // ���̴����α׷�
GLuint shaderprogram_ui; // ���̴����α׷�
GLuint shaderprogram_game_over;


void KeyPressed(unsigned char key, int x, int y);
void KeyUp(unsigned char key, int x, int y);

void Timerfunction(int value);

GLUquadric* qobj; // Quadric Object ������ 

enum Camera { first_p_view, third_p_view };
Camera d = third_p_view;

enum State {in_game_state, game_over_state};
State state = in_game_state;


//----------------------------
GLfloat game_over_vertex[] = {
	1.0f,  1.0f, 0.0f,   1.0f, 0.0f, 0.0f,    1.0f, 1.0f,   // �������0 
	1.0f, -1.0f, 0.0f,   0.0f, 1.0f, 0.0f,    1.0f, 0.0f,   // �����ϴ�1 
	-1.0f, -1.0f, 0.0f,  0.0f, 0.0f, 1.0f,    0.0f, 0.0f,   // �����ϴ�2
	-1.0f,  1.0f, 0.0f,  1.0f, 1.0f, 0.0f,    0.0f, 1.0f    // �������3

};
GLubyte game_over_index[] = {
	0,3,2,
	1,2,0
};



//-------------------

GLfloat ground_vertex_normal[] = {
	-1.0f, -0.5f, -100.0f, 0.0f, 1.0f, 0.0f,
	-1.0f, -0.5f, 100.0f, 0.0f, 1.0f, 0.0f,
	1.0f, -0.5f, 100.0f, 0.0f, 1.0f, 0.0f,
	1.0f, -0.5f, -100.0f, 0.0f, 1.0f, 0.0f,
	-1.0f, -0.5f, -100.0f, 0.0f, 1.0f, 0.0f,
	1.0f, -0.5f, 100.0f, 0.0f, 1.0f, 0.0f
};

//-----------------------------
GLfloat tank_body_vertex_normal[] = {
	//�޸� 
   -0.25f, -0.25f, -0.5f,  0.0f,  0.0f, -1.0f,
	0.25f, -0.25f, -0.5f,  0.0f,  0.0f, -1.0f,
	0.25f,  0.25f, -0.5f,  0.0f,  0.0f, -1.0f,
	0.25f,  0.25f, -0.5f,  0.0f,  0.0f, -1.0f,
   -0.25f,  0.25f, -0.5f,  0.0f,  0.0f, -1.0f,
   -0.25f, -0.25f, -0.5f,  0.0f,  0.0f, -1.0f,

   //�ո�
   -0.25f, -0.25f,  0.5f,  0.0f,  0.0f,  1.0f,
	0.25f, -0.25f,  0.5f,  0.0f,  0.0f,  1.0f,
	0.25f,  0.25f,  0.5f,  0.0f,  0.0f,  1.0f,
	0.25f,  0.25f,  0.5f,  0.0f,  0.0f,  1.0f,
   -0.25f,  0.25f,  0.5f,  0.0f,  0.0f,  1.0f,
   -0.25f, -0.25f,  0.5f,  0.0f,  0.0f,  1.0f,

   //���ʸ�
   -0.25f,  0.25f,  0.5f, -1.0f,  0.0f,  0.0f,
   -0.25f,  0.25f, -0.5f, -1.0f,  0.0f,  0.0f,
   -0.25f, -0.25f, -0.5f, -1.0f,  0.0f,  0.0f,
   -0.25f, -0.25f, -0.5f, -1.0f,  0.0f,  0.0f,
   -0.25f, -0.25f,  0.5f, -1.0f,  0.0f,  0.0f,
   -0.25f,  0.25f,  0.5f, -1.0f,  0.0f,  0.0f,

   //�����ʸ�
	0.25f,  0.25f,  0.5f,  1.0f,  0.0f,  0.0f,
	0.25f,  0.25f, -0.5f,  1.0f,  0.0f,  0.0f,
	0.25f, -0.25f, -0.5f,  1.0f,  0.0f,  0.0f,
	0.25f, -0.25f, -0.5f,  1.0f,  0.0f,  0.0f,
	0.25f, -0.25f,  0.5f,  1.0f,  0.0f,  0.0f,
	0.25f,  0.25f,  0.5f,  1.0f,  0.0f,  0.0f,

	//�ظ�
	-0.25f, -0.25f, -0.5f,  0.0f, -1.0f,  0.0f,
	 0.25f, -0.25f, -0.5f,  0.0f, -1.0f,  0.0f,
	 0.25f, -0.25f,  0.5f,  0.0f, -1.0f,  0.0f,
	 0.25f, -0.25f,  0.5f,  0.0f, -1.0f,  0.0f,
	-0.25f, -0.25f,  0.5f,  0.0f, -1.0f,  0.0f,
	-0.25f, -0.25f, -0.5f,  0.0f, -1.0f,  0.0f,

	//����
	-0.25f,  0.25f, -0.5f,  0.0f,  1.0f,  0.0f,
	 0.25f,  0.25f, -0.5f,  0.0f,  1.0f,  0.0f,
	 0.25f,  0.25f,  0.5f,  0.0f,  1.0f,  0.0f,
	 0.25f,  0.25f,  0.5f,  0.0f,  1.0f,  0.0f,
	-0.25f,  0.25f,  0.5f,  0.0f,  1.0f,  0.0f,
	-0.25f,  0.25f, -0.5f,  0.0f,  1.0f,  0.0f
};

//-----------------------------

//---------------------------------------------
GLfloat light_pos_norm_vertex[] = {
	//�޸�
   -0.25f, -0.25f, -0.25f,  0.0f,  0.0f, -1.0f,
	0.25f, -0.25f, -0.25f,  0.0f,  0.0f, -1.0f,
	0.25f,  0.25f, -0.25f,  0.0f,  0.0f, -1.0f,
	0.25f,  0.25f, -0.25f,  0.0f,  0.0f, -1.0f,
   -0.25f,  0.25f, -0.25f,  0.0f,  0.0f, -1.0f,
   -0.25f, -0.25f, -0.25f,  0.0f,  0.0f, -1.0f,

   //�ո�
   -0.25f, -0.25f,  0.25f,  0.0f,  0.0f,  1.0f,
	0.25f, -0.25f,  0.25f,  0.0f,  0.0f,  1.0f,
	0.25f,  0.25f,  0.25f,  0.0f,  0.0f,  1.0f,
	0.25f,  0.25f,  0.25f,  0.0f,  0.0f,  1.0f,
   -0.25f,  0.25f,  0.25f,  0.0f,  0.0f,  1.0f,
   -0.25f, -0.25f,  0.25f,  0.0f,  0.0f,  1.0f,

   //���ʸ�
   -0.25f,  0.25f,  0.25f, -1.0f,  0.0f,  0.0f,
   -0.25f,  0.25f, -0.25f, -1.0f,  0.0f,  0.0f,
   -0.25f, -0.25f, -0.25f, -1.0f,  0.0f,  0.0f,
   -0.25f, -0.25f, -0.25f, -1.0f,  0.0f,  0.0f,
   -0.25f, -0.25f,  0.25f, -1.0f,  0.0f,  0.0f,
   -0.25f,  0.25f,  0.25f, -1.0f,  0.0f,  0.0f,

   //�����ʸ�
	0.25f,  0.25f,  0.25f,  1.0f,  0.0f,  0.0f,
	0.25f,  0.25f, -0.25f,  1.0f,  0.0f,  0.0f,
	0.25f, -0.25f, -0.25f,  1.0f,  0.0f,  0.0f,
	0.25f, -0.25f, -0.25f,  1.0f,  0.0f,  0.0f,
	0.25f, -0.25f,  0.25f,  1.0f,  0.0f,  0.0f,
	0.25f,  0.25f,  0.25f,  1.0f,  0.0f,  0.0f,

	//�ظ�
	-0.25f, -0.25f, -0.25f,  0.0f, -1.0f,  0.0f,
	 0.25f, -0.25f, -0.25f,  0.0f, -1.0f,  0.0f,
	 0.25f, -0.25f,  0.25f,  0.0f, -1.0f,  0.0f,
	 0.25f, -0.25f,  0.25f,  0.0f, -1.0f,  0.0f,
	-0.25f, -0.25f,  0.25f,  0.0f, -1.0f,  0.0f,
	-0.25f, -0.25f, -0.25f,  0.0f, -1.0f,  0.0f,

	//����
	-0.25f,  0.25f, -0.25f,  0.0f,  1.0f,  0.0f,
	 0.25f,  0.25f, -0.25f,  0.0f,  1.0f,  0.0f,
	 0.25f,  0.25f,  0.25f,  0.0f,  1.0f,  0.0f,
	 0.25f,  0.25f,  0.25f,  0.0f,  1.0f,  0.0f,
	-0.25f,  0.25f,  0.25f,  0.0f,  1.0f,  0.0f,
	-0.25f,  0.25f, -0.25f,  0.0f,  1.0f,  0.0f

};

GLfloat obs1_vertex_normal[] = {
	//�޸�
   -0.15f, -0.15f, -0.15f,  0.0f,  0.0f, -1.0f,
	0.15f, -0.15f, -0.15f,  0.0f,  0.0f, -1.0f,
	0.15f,  0.15f, -0.15f,  0.0f,  0.0f, -1.0f,
	0.15f,  0.15f, -0.15f,  0.0f,  0.0f, -1.0f,
   -0.15f,  0.15f, -0.15f,  0.0f,  0.0f, -1.0f,
   -0.15f, -0.15f, -0.15f,  0.0f,  0.0f, -1.0f,

   //�ո�
   -0.15f, -0.15f,  0.15f,  0.0f,  0.0f,  1.0f,
	0.15f, -0.15f,  0.15f,  0.0f,  0.0f,  1.0f,
	0.15f,  0.15f,  0.15f,  0.0f,  0.0f,  1.0f,
	0.15f,  0.15f,  0.15f,  0.0f,  0.0f,  1.0f,
   -0.15f,  0.15f,  0.15f,  0.0f,  0.0f,  1.0f,
   -0.15f, -0.15f,  0.15f,  0.0f,  0.0f,  1.0f,

   //���ʸ�
   -0.15f,  0.15f,  0.15f, -1.0f,  0.0f,  0.0f,
   -0.15f,  0.15f, -0.15f, -1.0f,  0.0f,  0.0f,
   -0.15f, -0.15f, -0.15f, -1.0f,  0.0f,  0.0f,
   -0.15f, -0.15f, -0.15f, -1.0f,  0.0f,  0.0f,
   -0.15f, -0.15f,  0.15f, -1.0f,  0.0f,  0.0f,
   -0.15f,  0.15f,  0.15f, -1.0f,  0.0f,  0.0f,

   //�����ʸ�
	0.15f,  0.15f,  0.15f,  1.0f,  0.0f,  0.0f,
	0.15f,  0.15f, -0.15f,  1.0f,  0.0f,  0.0f,
	0.15f, -0.15f, -0.15f,  1.0f,  0.0f,  0.0f,
	0.15f, -0.15f, -0.15f,  1.0f,  0.0f,  0.0f,
	0.15f, -0.15f,  0.15f,  1.0f,  0.0f,  0.0f,
	0.15f,  0.15f,  0.15f,  1.0f,  0.0f,  0.0f,

	//�ظ�
	-0.15f, -0.15f, -0.15f,  0.0f, -1.0f,  0.0f,
	 0.15f, -0.15f, -0.15f,  0.0f, -1.0f,  0.0f,
	 0.15f, -0.15f,  0.15f,  0.0f, -1.0f,  0.0f,
	 0.15f, -0.15f,  0.15f,  0.0f, -1.0f,  0.0f,
	-0.15f, -0.15f,  0.15f,  0.0f, -1.0f,  0.0f,
	-0.15f, -0.15f, -0.15f,  0.0f, -1.0f,  0.0f,

	//����
	-0.15f,  0.15f, -0.15f,  0.0f,  1.0f,  0.0f,
	 0.15f,  0.15f, -0.15f,  0.0f,  1.0f,  0.0f,
	 0.15f,  0.15f,  0.15f,  0.0f,  1.0f,  0.0f,
	 0.15f,  0.15f,  0.15f,  0.0f,  1.0f,  0.0f,
	-0.15f,  0.15f,  0.15f,  0.0f,  1.0f,  0.0f,
	-0.15f,  0.15f, -0.15f,  0.0f,  1.0f,  0.0f
};

GLfloat tree_vertex_normal[]{
	//�޸�
   -0.15f, -0.5f, -0.15f,  0.0f,  0.0f, -1.0f,
	0.15f, -0.5f, -0.15f,  0.0f,  0.0f, -1.0f,
	0.15f,  0.5f, -0.15f,  0.0f,  0.0f, -1.0f,
	0.15f,  0.5f, -0.15f,  0.0f,  0.0f, -1.0f,
   -0.15f,  0.5f, -0.15f,  0.0f,  0.0f, -1.0f,
   -0.15f, -0.5f, -0.15f,  0.0f,  0.0f, -1.0f,

   //�ո�
   -0.15f, -0.5f,  0.15f,  0.0f,  0.0f,  1.0f,
	0.15f, -0.5f,  0.15f,  0.0f,  0.0f,  1.0f,
	0.15f,  0.5f,  0.15f,  0.0f,  0.0f,  1.0f,
	0.15f,  0.5f,  0.15f,  0.0f,  0.0f,  1.0f,
   -0.15f,  0.5f,  0.15f,  0.0f,  0.0f,  1.0f,
   -0.15f, -0.5f,  0.15f,  0.0f,  0.0f,  1.0f,

   //���ʸ�
   -0.15f,  0.5f,  0.15f, -1.0f,  0.0f,  0.0f,
   -0.15f,  0.5f, -0.15f, -1.0f,  0.0f,  0.0f,
   -0.15f, -0.5f, -0.15f, -1.0f,  0.0f,  0.0f,
   -0.15f, -0.5f, -0.15f, -1.0f,  0.0f,  0.0f,
   -0.15f, -0.5f,  0.15f, -1.0f,  0.0f,  0.0f,
   -0.15f,  0.5f,  0.15f, -1.0f,  0.0f,  0.0f,

   //�����ʸ�
	0.15f,  0.5f,  0.15f,  1.0f,  0.0f,  0.0f,
	0.15f,  0.5f, -0.15f,  1.0f,  0.0f,  0.0f,
	0.15f, -0.5f, -0.15f,  1.0f,  0.0f,  0.0f,
	0.15f, -0.5f, -0.15f,  1.0f,  0.0f,  0.0f,
	0.15f, -0.5f,  0.15f,  1.0f,  0.0f,  0.0f,
	0.15f,  0.5f,  0.15f,  1.0f,  0.0f,  0.0f,

	//�ظ�
	-0.15f, -0.5f, -0.15f,  0.0f, -1.0f,  0.0f,
	 0.15f, -0.5f, -0.15f,  0.0f, -1.0f,  0.0f,
	 0.15f, -0.5f,  0.15f,  0.0f, -1.0f,  0.0f,
	 0.15f, -0.5f,  0.15f,  0.0f, -1.0f,  0.0f,
	-0.15f, -0.5f,  0.15f,  0.0f, -1.0f,  0.0f,
	-0.15f, -0.5f, -0.15f,  0.0f, -1.0f,  0.0f,

	//����
	-0.15f,  0.5f, -0.15f,  0.0f,  1.0f,  0.0f,
	 0.15f,  0.5f, -0.15f,  0.0f,  1.0f,  0.0f,
	 0.15f,  0.5f,  0.15f,  0.0f,  1.0f,  0.0f,
	 0.15f,  0.5f,  0.15f,  0.0f,  1.0f,  0.0f,
	-0.15f,  0.5f,  0.15f,  0.0f,  1.0f,  0.0f,
	-0.15f,  0.5f, -0.15f,  0.0f,  1.0f,  0.0f
};

float body_x = 0;
float body_y = 0;
float body_z = 0;


int cnt;

float player_bb() {
	return body_x - 0.25f, body_y - 0.25f, body_z - 0.25f,
		body_x + 0.25f, body_y + 0.25f, body_z + 0.25f;
}




//��ֹ� Ŭ����----------------------------------
class Obstacle {
	float obs_x, obs_z = 0; //�⺻ ��ֹ�
	float obs_y = 0;
public:
	Obstacle(float x, float y, float z) :obs_x{ x }, obs_y{ y }, obs_z{ z } {};

	float get_obs_x() {
		return obs_x;
	}
	float get_obs_y() {
		return obs_y;
	}
	float get_obs_z() {
		return obs_z;
	}
	float get_bb() {
		return get_obs_x() - 0.15f, get_obs_y() - 0.15f, get_obs_z() - 0.15f,
			get_obs_x() + 0.15f, get_obs_y() + 0.15f, get_obs_z() + 0.15f;
	}
	
	bool update() {
		
		obs_z += 0.1f;
		if (obs_z > 50.0f)
			return true;
		return false;
	}
	void make_obs1() {
		//��ֹ� 1
		//��-----------------------------------
		glm::mat4 obs1_move = glm::mat4(1.0f);
		glm::mat4 obs1_first_state = glm::mat4(1.0f);

		obs1_first_state = glm::translate(obs1_first_state, glm::vec3(obs_x, obs_y, obs_z));

		obs1_move = obs1_first_state;

		unsigned int modelLocation3 = glGetUniformLocation(shaderprogram, "modelTransform");
		glUniformMatrix4fv(modelLocation3, 1, GL_FALSE, glm::value_ptr(obs1_move));


		//����-------------------------------------------------------------------
		int lightPosLocation3 = glGetUniformLocation(shaderprogram, "lightPos"); //--- lightPos ������
		glUniform3f(lightPosLocation3, 0.0f, 2.0f, 5.0f);
		int lightColorLocation3 = glGetUniformLocation(shaderprogram, "lightColor"); //--- lightColor������
		glUniform3f(lightColorLocation3, 1.0f, 1.0f, 1.0f);
		int objColorLocation3 = glGetUniformLocation(shaderprogram, "objectColor"); //--- object Color������
		glUniform3f(objColorLocation3, 1.0f, 1.0f, 0.0f);
		int personLocation3 = glGetUniformLocation(shaderprogram, "viewPos");
		glUniform3f(personLocation3, 0.0f, 0.0f, 1.0f);

		glBindVertexArray(obs_vao[0]);
		glDrawArrays(GL_TRIANGLES, 0, 36);

	}

};
class ring_Obstacle {
	float ring_x, ring_z; //�� ��ֹ�
	float ring_y;

public:
	ring_Obstacle(float x, float y, float z) : ring_x{ x }, ring_y{ y }, ring_z{ z } {}
	bool update_ring() {
		ring_z += 0.15f;
		if (ring_z > 50.0f)
			return true;
		return false;
	}
	void make_obs2() {
		glm::mat4 ring_move = glm::mat4(1.0f);
		glm::mat4 ring_first_state = glm::mat4(1.0f);

		ring_first_state = glm::translate(ring_first_state, glm::vec3(ring_x, ring_y, ring_z));
		ring_move = ring_first_state;

		unsigned int modelLocation4 = glGetUniformLocation(shaderprogram, "modelTransform");
		glUniformMatrix4fv(modelLocation4, 1, GL_FALSE, glm::value_ptr(ring_move));

		//����-------------------------------------------------------------------
		int lightPosLocation4 = glGetUniformLocation(shaderprogram, "lightPos"); //--- lightPos ������
		glUniform3f(lightPosLocation4, 0.0f, 2.0f, 5.0f);
		int lightColorLocation4 = glGetUniformLocation(shaderprogram, "lightColor"); //--- lightColor������
		glUniform3f(lightColorLocation4, 1.0f, 1.0f, 1.0f);
		int objColorLocation4 = glGetUniformLocation(shaderprogram, "objectColor"); //--- object Color������
		glUniform3f(objColorLocation4, 1.0f, 1.0f, 0.0f);
		int personLocation4 = glGetUniformLocation(shaderprogram, "viewPos");
		glUniform3f(personLocation4, 0.0f, 0.0f, 1.0f);

		qobj = gluNewQuadric(); //��ü�� �����Ѵ�.
		gluQuadricDrawStyle(qobj, GLU_FILL); //��� �׸��� ���Ѵ�

		gluQuadricNormals(qobj, GLU_SMOOTH); //(���� ����)
		gluQuadricOrientation(qobj, GLU_OUTSIDE); //(���� ����)

		gluDisk(qobj, 0.4f, 0.5f, 50, 50);


	}
};

class oc_Obstacle {
	float oc_x, oc_z = 0;
	float oc_y = 0;
	float oc_dx = 0.01f;

	float oc_x2, oc_z2 = 0;
	float oc_y2 = 0;

	float oc_dx2 = -0.01f;
public:
	oc_Obstacle(float xl, float yl, float zl, float xr, float yr, float zr) : oc_x{ xl }, oc_y{ yl },oc_z{ zl },
		oc_x2{ xr }, oc_y2{ yr }, oc_z2{ zr } {}

	float get_oc_x() {
		return oc_x;
	}
	float get_oc_y() {
		return oc_y;
	}
	float get_oc_z() {
		return oc_z;
	}

	float get_oc_x2() {
		return oc_x2;
	}
	float get_oc_y2() {
		return oc_y2;
	}
	float get_oc_z2() {
		return oc_z2;
	}


	bool update_oc() {
		//��
		oc_z += 0.1f;
		oc_x += oc_dx;


		if (oc_x >= -0.1f || oc_x <= -0.7f) {
			oc_dx *= -1;
		}

		if (oc_z > 50.0f)
			return true;
		return false;


	}
	bool update_oc2() {
		//��
		oc_z2 += 0.1f;
		oc_x2 += oc_dx2;
		if (oc_x2 <= 0.1f || oc_x2 >= 0.7f) {
			oc_dx2 *= -1;
		}
		if (oc_z2 > 50.0f)
			return true;
		return false;
	}
	void make_obs3() {
		//��-----------------------------------
		glm::mat4 obs_oc_move = glm::mat4(1.0f);
		glm::mat4 obs_oc_first_state = glm::mat4(1.0f);

		obs_oc_first_state = glm::translate(obs_oc_first_state, glm::vec3(oc_x, -0.25f, oc_z));

		obs_oc_move = obs_oc_first_state;

		unsigned int modelLocation7 = glGetUniformLocation(shaderprogram, "modelTransform");
		glUniformMatrix4fv(modelLocation7, 1, GL_FALSE, glm::value_ptr(obs_oc_move));

		//����-------------------------------------------------------------------
		int lightPosLocation7 = glGetUniformLocation(shaderprogram, "lightPos"); //--- lightPos ������
		glUniform3f(lightPosLocation7, 0.0f, 2.0f, 5.0f);
		int lightColorLocation7 = glGetUniformLocation(shaderprogram, "lightColor"); //--- lightColor������
		glUniform3f(lightColorLocation7, 1.0f, 1.0f, 1.0f);
		int objColorLocation7 = glGetUniformLocation(shaderprogram, "objectColor"); //--- object Color������
		glUniform3f(objColorLocation7, 0.0f, 1.0f, 1.0f);
		int personLocation7 = glGetUniformLocation(shaderprogram, "viewPos");
		glUniform3f(personLocation7, 0.0f, 0.0f, 1.0f);

		glBindVertexArray(obs_vao[1]);
		glDrawArrays(GL_TRIANGLES, 0, 36);

		//
		//��-----------------------------------
		glm::mat4 obs_oc2_move = glm::mat4(1.0f);
		glm::mat4 obs_oc2_first_state = glm::mat4(1.0f);

		obs_oc2_first_state = glm::translate(obs_oc2_first_state, glm::vec3(oc_x2, -0.25f, oc_z2));

		obs_oc2_move = obs_oc2_first_state;

		unsigned int modelLocation8 = glGetUniformLocation(shaderprogram, "modelTransform");
		glUniformMatrix4fv(modelLocation8, 1, GL_FALSE, glm::value_ptr(obs_oc2_move));

		//����-------------------------------------------------------------------
		int lightPosLocation8 = glGetUniformLocation(shaderprogram, "lightPos"); //--- lightPos ������
		glUniform3f(lightPosLocation8, 0.0f, 2.0f, 5.0f);
		int lightColorLocation8 = glGetUniformLocation(shaderprogram, "lightColor"); //--- lightColor������
		glUniform3f(lightColorLocation8, 1.0f, 1.0f, 1.0f);
		int objColorLocation8 = glGetUniformLocation(shaderprogram, "objectColor"); //--- object Color������
		glUniform3f(objColorLocation8, 0.0f, 1.0f, 1.0f);
		int personLocation8 = glGetUniformLocation(shaderprogram, "viewPos");
		glUniform3f(personLocation8, 0.0f, 0.0f, 1.0f);

		glBindVertexArray(obs_vao[2]);
		glDrawArrays(GL_TRIANGLES, 0, 36);
	}
};



//float tree_z = -50.0f;

float tree_color_r;
float tree_color_g;
float tree_color_b;


class Tree {
	float x, z;
public:
	Tree(float x, float z) :x{ x }, z{ z } {};
	bool update() {
		z += 0.2f; //���� �ٰ���
		if (z > 100.0f)
			return true;
		return false;
	}
	void draw() {
		glm::mat4 tree_move = glm::mat4(1.0f);
		glm::mat4 tree_first_state = glm::mat4(1.0f);

		tree_first_state = glm::translate(tree_first_state, glm::vec3(x, 0.0f, z));
		tree_move = tree_first_state;

		unsigned int modelLocation5 = glGetUniformLocation(shaderprogram, "modelTransform");
		glUniformMatrix4fv(modelLocation5, 1, GL_FALSE, glm::value_ptr(tree_move));

		//����-------------------------------------------------------------------
		int lightPosLocation5 = glGetUniformLocation(shaderprogram, "lightPos"); //--- lightPos ������
		glUniform3f(lightPosLocation5, 0.0f, 0.0f, 5.0f);
		int lightColorLocation5 = glGetUniformLocation(shaderprogram, "lightColor"); //--- lightColor������
		glUniform3f(lightColorLocation5, 1.0f, 1.0f, 1.0f);
		int objColorLocation5 = glGetUniformLocation(shaderprogram, "objectColor"); //--- object Color������
		glUniform3f(objColorLocation5, 1.0f, 1.0f, 0.5f);
		int personLocation5 = glGetUniformLocation(shaderprogram, "viewPos");
		glUniform3f(personLocation5, 0.0f, 0.0f, 5.0f);

		glBindVertexArray(tree_vao[0]);
		glDrawArrays(GL_TRIANGLES, 0, 36);

		//������------------------------
		glm::mat4 leaf_move = glm::mat4(1.0f);
		glm::mat4 leaf_first_state = glm::mat4(1.0f);

		leaf_first_state = glm::translate(leaf_first_state, glm::vec3(x, 0.5f, z));
		leaf_move = leaf_first_state;

		unsigned int modelLocation6 = glGetUniformLocation(shaderprogram, "modelTransform");
		glUniformMatrix4fv(modelLocation6, 1, GL_FALSE, glm::value_ptr(leaf_move));


		//����-------------------------------------------------------------------
		int lightPosLocation6 = glGetUniformLocation(shaderprogram, "lightPos"); //--- lightPos ������
		glUniform3f(lightPosLocation6, 0.0f, 0.0f, 5.0f);
		int lightColorLocation6 = glGetUniformLocation(shaderprogram, "lightColor"); //--- lightColor������
		glUniform3f(lightColorLocation6, 1.0f, 1.0f, 1.0f);
		int objColorLocation6 = glGetUniformLocation(shaderprogram, "objectColor"); //--- object Color������
		glUniform3f(objColorLocation6, tree_color_r, tree_color_g, tree_color_b);
		int personLocation6 = glGetUniformLocation(shaderprogram, "viewPos");
		glUniform3f(personLocation6, 0.0f, 0.0f, 5.0f);

		qobj = gluNewQuadric(); //��ü�� �����Ѵ�.
		gluQuadricDrawStyle(qobj, GLU_FILL); //��� �׸��� ���Ѵ�

		gluQuadricNormals(qobj, GLU_SMOOTH); //(���� ����)
		gluQuadricOrientation(qobj, GLU_OUTSIDE); //(���� ����)
		gluSphere(qobj, 0.4f, 20, 20);

	}
};

class Snow
{
	float x, y, z;
public:
	Snow(float x, float y, float z) :x{ x }, y{ y }, z{ z } {}

	bool update()
	{
		y -= 0.01f;
		if (y <= 0)
			return true;
		return false;
	}
	void draw() {
		qobj = gluNewQuadric(); //��ü�� �����Ѵ�.
		gluQuadricDrawStyle(qobj, GL_FILL); //��� �׸��� ���Ѵ�

		gluQuadricNormals(qobj, GLU_SMOOTH); //(���� ����)
		gluQuadricOrientation(qobj, GLU_OUTSIDE); //(���� ����)

		glm::mat4 snow_move = glm::mat4(1.0f);
		snow_move = glm::translate(snow_move, glm::vec3(x, y, z));

		unsigned int modelLocation3 = glGetUniformLocation(shaderprogram, "modelTransform");
		glUniformMatrix4fv(modelLocation3, 1, GL_FALSE, glm::value_ptr(snow_move));

		//����-------------------------------------------------------------------
		int lightPosLocation3 = glGetUniformLocation(shaderprogram, "lightPos"); //--- lightPos ������
		glUniform3f(lightPosLocation3, 1.2, 1.0, 1.0);
		int lightColorLocation3 = glGetUniformLocation(shaderprogram, "lightColor"); //--- lightColor������
		glUniform3f(lightColorLocation3, 1.0f, 1.0f, 1.0f);
		int objColorLocation3 = glGetUniformLocation(shaderprogram, "objectColor"); //--- object Color������
		glUniform3f(objColorLocation3, 1.0f, 1.0f, 1.0f);
		int personLocation3 = glGetUniformLocation(shaderprogram, "viewPos");
		glUniform3f(personLocation3, 0.0f, 0.0f, 3.0f);

		gluSphere(qobj, 0.01f, 10, 10);
	}
};

vector<Tree> trees;
vector<Obstacle> obs;
vector<ring_Obstacle> ring_obs;
vector<oc_Obstacle> oc_obs;

vector<Snow> snow;


GLuint compile_shader(const char *vs, const char*fs)
{
	GLuint tempSP; // ���̴����α׷�


	vertexsource = filetobuf(vs);
	fragmentsource = filetobuf(fs);



	//���ؽ� ���̴� ��ü �����
	vertexshader = glCreateShader(GL_VERTEX_SHADER);


	//���̴� �ڵ带 ���̴� ��ü�� �ֱ�: GL�� ��������. (�ҽ��ڵ�: ���ڿ�)
	glShaderSource(vertexshader, 1, (const GLchar**)&vertexsource, 0);

	// ���ؽ����̴��������ϱ�
	glCompileShader(vertexshader);


	// ������������ε����������: ����üũ 

	GLint IsCompiled_VS;
	GLint maxLength;
	GLchar* vertexInfoLog;
	glGetShaderiv(vertexshader, GL_COMPILE_STATUS, &IsCompiled_VS);
	if (IsCompiled_VS == FALSE)
	{
		glGetShaderiv(vertexshader, GL_INFO_LOG_LENGTH, &maxLength);
		vertexInfoLog = (char *)malloc(maxLength);
		glGetShaderInfoLog(vertexshader, maxLength, &maxLength, vertexInfoLog);
		std::cout << vertexInfoLog;
		free(vertexInfoLog);
		return false;
	}

	//---�����׸�Ʈ���̴���ü����� 
	fragmentshader = glCreateShader(GL_FRAGMENT_SHADER);

	// ���̴��ڵ带���̴���ü���ֱ�: GL�κ�������. 
	glShaderSource(fragmentshader, 1, (const GLchar**)&fragmentsource, 0);

	// �����׸�Ʈ���̴������� 
	glCompileShader(fragmentshader);

	GLint IsCompiled_FS;
	GLchar*  fragmentInfoLog;

	// ������������ε����������: �����Ͽ���üũ
	glGetShaderiv(fragmentshader, GL_COMPILE_STATUS, &IsCompiled_FS);
	if (IsCompiled_FS == FALSE)
	{
		glGetShaderiv(fragmentshader, GL_INFO_LOG_LENGTH, &maxLength);
		fragmentInfoLog = (char *)malloc(maxLength);
		glGetShaderInfoLog(fragmentshader, maxLength, &maxLength, fragmentInfoLog);
		std::cout << fragmentInfoLog;
		free(fragmentInfoLog);
		return false;
	}


	// ���ؽ����̴��������׸�Ʈ���̴��������ϵư�, ���������°�� 
	// GL ���̴���ü�������μ��̴�����ũ�Ѵ�. 
	// ���̴����α׷���ü�����
	tempSP = glCreateProgram();

	// ���̴������̴����α׷���ü�����δ�. 
	glAttachShader(tempSP, vertexshader);
	glAttachShader(tempSP, fragmentshader);

	// in_Position: �ε��� 0, 
	// in_Color: �ε��� 1 ���μӼ��ε��������ε��Ѵ�. 
	// �Ӽ���ġ�����α׷���ũ���������Ѵ�.
	//glBindAttribLocation(tempSP, 0, "in_Position"); 
	//glBindAttribLocation(tempSP, 1, "in_Color");

	// ���α׷���ũ 
	// �̶�, ���̴����α׷����������̹��̳ʸ��ڵ尡���̴������Ͽ� 
	// �����ǰ���ڵ尡 GPU�����ε�� (���������ٸ�) 
	glLinkProgram(tempSP);

	glDeleteShader(vertexshader); // ���̴����α׷�����ũ�Ͽ����̴���ü��ü�»������� 
	glDeleteShader(fragmentshader);




	GLint IsLinked;
	GLchar* tempSPInfoLog;
	// ��ũ���Ǿ�����üũ�ϱ� 
	glGetProgramiv(tempSP, GL_LINK_STATUS, (int *)&IsLinked);
	if (IsLinked == FALSE) {
		glGetProgramiv(tempSP, GL_INFO_LOG_LENGTH, &maxLength);
		tempSPInfoLog = (char *)malloc(maxLength);
		glGetProgramInfoLog(tempSP, maxLength, &maxLength, tempSPInfoLog);
		free(tempSPInfoLog);
		return false;
	}
	return tempSP;
}

GLuint texture1, texture_end;

void initTexture(const char *imgStr, GLuint& textureID) {

	//textureID
	glGenTextures(1, &textureID); //---�ؽ�ó���� 
	glBindTexture(GL_TEXTURE_2D, textureID); //---�ؽ�ó���ε�

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT); //---������ε����ؽ�ó��ü�ǼӼ������ϱ� 
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

	int width, height, nrChannels;
	unsigned char *data = stbi_load(imgStr, &width, &height, &nrChannels, 0); //---�ؽ�ó�λ���Һ�Ʈ���̹����ε��ϱ�

	if (data)
	{
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data);
		glGenerateMipmap(GL_TEXTURE_2D);
		std::cout << "Succeed texture" << std::endl;

	}
	else
	{
		std::cout << "Failed to load texture" << std::endl;
	}
}




int main(int argc, char** argv) // ������ ����ϰ� �ݹ��Լ� ���� 
{

	//--- ������ �����ϱ� 
	glutInit(&argc, argv); // glut �ʱ�ȭ 
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH); // ���÷��� ��� ���� 
	glutInitWindowPosition(0, 0); // �������� ��ġ ���� 
	glutInitWindowSize(1000, 800); // �������� ũ�� ���� 
	glutCreateWindow("TermProject_2017180012_jypark"); // ������ ���� (������ �̸�) 

	//--- GLEW �ʱ�ȭ�ϱ� 
	glewExperimental = GL_TRUE;
	if (glewInit() != GLEW_OK) // glew �ʱ�ȭ 
	{
		cerr << "Unable to initialize GLEW" << endl;
		exit(EXIT_FAILURE);
	}
	else
		cout << "GLEW Initialized\n";

	shaderprogram = compile_shader("tp.glvs", "tp_fragment.glfs");
	shaderprogram_ui = compile_shader("test.glvs", "test.glfs");
	shaderprogram_game_over = compile_shader("game_over.glvs", "game_over.glfs");
	initTexture("numset.png", texture1);


	//-----------------------------------------------------------------------------
	//���ٴ�
	glGenVertexArrays(1, &ground_vao);
	glGenBuffers(1, &ground_vbo);


	glBindVertexArray(ground_vao);

	glBindBuffer(GL_ARRAY_BUFFER, ground_vbo);
	glBufferData(GL_ARRAY_BUFFER, sizeof(ground_vertex_normal), ground_vertex_normal, GL_STATIC_DRAW);

	//---��ġ�Ӽ�
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);
	//---�븻�Ӽ�
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);

	//-----------------------------------------------------------------------------
	//���ؽ� array ����
	glGenVertexArrays(1, cube_vao);
	glGenBuffers(1, cube_vbo);

	glBindVertexArray(cube_vao[0]);
	//����
	glBindBuffer(GL_ARRAY_BUFFER, cube_vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(tank_body_vertex_normal), tank_body_vertex_normal, GL_STATIC_DRAW);


	//---��ġ�Ӽ�
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);
	//---�븻�Ӽ�
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);

	//��ֹ�
	//-----------------------------------------------------------
	glGenVertexArrays(3, obs_vao);
	glGenBuffers(3, obs_vbo);

	glBindVertexArray(obs_vao[0]);
	//����
	glBindBuffer(GL_ARRAY_BUFFER, obs_vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(obs1_vertex_normal), obs1_vertex_normal, GL_STATIC_DRAW);

	//---��ġ�Ӽ�
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);
	//---�븻�Ӽ�
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);

	//Open & Close Obstacle
	glBindVertexArray(obs_vao[1]);
	//����
	glBindBuffer(GL_ARRAY_BUFFER, obs_vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(obs1_vertex_normal), obs1_vertex_normal, GL_STATIC_DRAW);

	//---��ġ�Ӽ�
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);
	//---�븻�Ӽ�
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);

	//
	glBindVertexArray(obs_vao[2]);
	//����
	glBindBuffer(GL_ARRAY_BUFFER, obs_vbo[2]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(obs1_vertex_normal), obs1_vertex_normal, GL_STATIC_DRAW);

	//---��ġ�Ӽ�
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);
	//---�븻�Ӽ�
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);





	//����
	//------------------------------------------------------------
	glGenVertexArrays(1, tree_vao);
	glGenBuffers(1, tree_vbo);

	glBindVertexArray(tree_vao[0]);
	//����
	glBindBuffer(GL_ARRAY_BUFFER, tree_vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(tree_vertex_normal), tree_vertex_normal, GL_STATIC_DRAW);

	//---��ġ�Ӽ�
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);
	//---�븻�Ӽ�
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);

	//--------------------------------------------------------------
	//Game Over
	glGenVertexArrays(1, &game_over_vao);
	glGenBuffers(1, &game_over_vbo);
	glGenBuffers(1, &game_over_ebo);


	glBindVertexArray(game_over_vao);
	

	glBindBuffer(GL_ARRAY_BUFFER, game_over_vbo);
	glBufferData(GL_ARRAY_BUFFER, sizeof(game_over_vertex), game_over_vertex, GL_STATIC_DRAW);

	//ebo
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, game_over_ebo); // GL_ELEMENT_ARRAY_BUFFER �����������ι��ε� 
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(game_over_index), game_over_index, GL_STATIC_DRAW);


	//---��ġ�Ӽ�
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)0);
	glEnableVertexAttribArray(0);

	//����
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);

	//�ؽ�ó ��ǥ
	glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(6 * sizeof(float)));
	glEnableVertexAttribArray(2);

	stbi_set_flip_vertically_on_load(true);
	initTexture("game_over.png", texture_end);

	//-----------------------------------------------------------
	glBindVertexArray(0);

	glEnable(GL_DEPTH_TEST);

	glutTimerFunc(10, Timerfunction, 1); //�ִϸ��̼�

	//Ű����
	glutKeyboardFunc(KeyPressed);
	glutKeyboardUpFunc(KeyUp);
	//glutSpecialFunc(SpeicalKey);

	glutDisplayFunc(drawScene); // ��� �Լ��� ����
	glutReshapeFunc(Reshape); // �ٽ� �׸��� �Լ� ����

	glutMainLoop(); // �̺�Ʈ ó�� ���� 


}




float player_angle = 0.f;

float middle_angle_x = 0.f;

float top_angle_z = 0.f;

int id;

float camera_pos_z = 7.0f;
float camera_pos_x = -1.0f;

float camera_dir_x = 0.0f;

float the = 0;
float new_the = 0;

float light_x = 1.2f;
float light_y = 1.0f;
float light_z = 2.0f;

//3��Ī
float c_pos_x = 0.0f;
float c_pos_y = 0.5f;
float c_pos_z = 0.0f;

//1��Ī
float c_pos_x_f = body_x;
float c_pos_y_f = body_y;
float c_pos_z_f = -body_z - 0.5f;

float c_pos_dx_f = 0.0f;
float c_pos_dy_f = 0.0f;
float c_pos_dz_f = 0.0f;
//-------------------


float player_x = 0.0f;
float player_y = 0.0f;
float player_z = 0.0f;

float body_dx = 0.0f;
float body_dy = 0.0f;
float body_dz = 0.0f;

float gravity = -0.01f;
float friction = -0.12f;
float player_acc = 0.05f;

float acc_x = 0.0f;
float acc_y = gravity;

int r_pressed = 0;
GLboolean p_pressed = false;
GLboolean jumping = false;



GLboolean l_pressed = false;
int l_pressed_count = 0;

GLboolean snowing = false;
void KeyPressed(unsigned char key, int x, int y) {
	switch (key) {
	case VK_ESCAPE:
		glutLeaveMainLoop();
		break;
	case 'q':
		glutLeaveMainLoop();
		break;
	case 'w':
		body_dz = -0.05f;
		c_pos_dz_f = -0.05f;
		break;
	case 'a':
		body_dx = -0.05f;
		c_pos_dx_f = -0.05f;

		break;
	case 's':
		body_dz = 0.05f;
		c_pos_dz_f = 0.05f;

		break;
	case 'd':
		body_dx = 0.05f;
		c_pos_dx_f = 0.05f;

		break;


	case VK_SPACE: //����
		if (body_y == 0) {
			body_dy = 0.15f;
		}
		
		break;

	case 'r':
		if (state == game_over_state) {
			state = in_game_state;

			player_angle = 0.f;
			middle_angle_x = 0.f;
			top_angle_z = 0.f;

			camera_pos_z = 7.0f;
			camera_pos_x = -1.0f;

			camera_dir_x = 0.0f;

			the = 0;
			new_the = 0;

			light_x = 1.2f;
			light_y = 1.0f;
			light_z = 2.0f;


			c_pos_x = 0.0f;
			c_pos_y = 0.5f;
			c_pos_z = 0.0f;


			c_pos_x_f = body_x;
			c_pos_y_f = body_y;
			c_pos_z_f = -body_z - 0.5f;

			c_pos_dx_f = 0.0f;
			c_pos_dy_f = 0.0f;
			c_pos_dz_f = 0.0f;
			//---------------


			player_x = 0.0f;
			player_y = 0.0f;
			player_z = 0.0f;

			body_dx = 0.0f;
			body_dy = 0.0f;
			body_dz = 0.0f;

			gravity = -0.01f;
			friction = -0.12f;
			player_acc = 0.05f;

			acc_x = 0.0f;
			acc_y = gravity;

			r_pressed = 0;

			p_pressed = false;
			jumping = false;

			body_x = 0;
			body_y = 0;
			body_z = 0;

			state = in_game_state;
			d = third_p_view;

			life = 10;

			t = 0;

			dis_l = 0;
			dis_r = 0;

			dis_oc_lr = 0;
			dis_oc_rl = 0;

			testnum = 0;

			body_bb_x = 0;

		}
	
		break;
	case 'p':

		break;

	case 'l':


		if (l_pressed_count > 10) {
			l_pressed = false;
		}
		else {
			l_pressed = true;
		}
		break;

	case '1': //1��Ī �������� ����
		d = first_p_view;
		break;
	case '3':
		d = third_p_view;
		break;
	case 'u':
		life -= 1;
		break;

	
	}
	glutPostRedisplay();

}

void KeyUp(unsigned char key, int x, int y) {
	switch (key) {

	case 'w':

		if (snowing == true) {
			;
		}
		else {
			body_dz = 0.0f;
			c_pos_dz_f = 0.0f;
		}

		break;
	case 'a':

		if (snowing == true) {
			;
		}
		else {
			body_dx = 0.0f;
			c_pos_dx_f = 0.0f;
		}

		break;
	case 's':

		if (snowing == true) {
			;
		}
		else {
			body_dz = 0.0f;
			c_pos_dz_f = 0.0f;
		}

		break;
	case 'd':

		if (snowing == true) {
			;
		}
		else {
			body_dx = 0.0f;
			c_pos_dx_f = 0.0f;
		}

		break;
	case 'l':
		l_pressed_count++;

		l_pressed = false;
		break;
	case VK_SPACE: //����
		jumping = true;

		break;
		

	}
	glutPostRedisplay();

}


vector<Tree>::iterator iter;
vector<Obstacle>::iterator obs_iter;
vector<ring_Obstacle>::iterator ring_iter;
vector<oc_Obstacle>::iterator oc_iter;

vector<Snow>::iterator sn_iter;

float ground_color_r;
float ground_color_g;
float ground_color_b;

//return offset
int drawNum(int num, int offset, float scale)
{

	int nextval = num / 10;
	int id = num % 10;

	if (nextval)
		offset = drawNum(num / 10, offset, scale);

	static int asdf{ 0 };
	int uiCharIDuniform = glGetUniformLocation(shaderprogram_ui, "uiCharid"); 
	int uioffsetuniform = glGetUniformLocation(shaderprogram_ui, "offset"); 
	glUniform1i(uiCharIDuniform, id);
	glUniform3f(uioffsetuniform, offset, scale, 800.0 / 1000.0);


	glDrawArrays(GL_QUADS, 0, 4);
	offset++;

	return offset;
}
void drawInt(int num, float posx, float posy, float scale,
	float colorx = 1, float colory = 1, float colorz = 1)
{
	int uiposuniform = glGetUniformLocation(shaderprogram_ui, "pos"); 
	int uicoloruniform = glGetUniformLocation(shaderprogram_ui, "color"); 
	glUniform2f(uiposuniform, posx, posy);
	glUniform3f(uicoloruniform, colorx, colory, colorz);
	drawNum(num, 0, scale);
}

GLvoid drawScene() // �ݹ� �Լ�: ��� 
{
	if (state == in_game_state) {
		glClearColor(0.1f, 0.1f, 0.1f, 1.0f);

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		glUseProgram(shaderprogram);



		if (d == third_p_view) {
			//���� ī�޶�------------------------
			glm::vec3 cameraPos = glm::vec3(0.0f, c_pos_y, 7.0f);
			glm::vec3 cameraDirection = glm::vec3(0.0f, 0.0f, 0.0f);
			glm::vec3 cameraUp = glm::vec3(0.0f, 1.0f, 0.0f);
			glm::mat4 view = glm::mat4(1.0f);
			view = glm::lookAt(cameraPos, cameraDirection, cameraUp);

			unsigned int viewLocation = glGetUniformLocation(shaderprogram, "viewTransform");
			glUniformMatrix4fv(viewLocation, 1, GL_FALSE, &view[0][0]);
		}
		if (d == first_p_view) {
			if (l_pressed == true) {
				//���� ī�޶�------------------------
				glm::vec3 cameraPos = glm::vec3(c_pos_x_f, body_y - 0.25f, c_pos_z_f);
				glm::vec3 cameraDirection = glm::vec3(0.0f, 0.0f, -50.0f);
				glm::vec3 cameraUp = glm::vec3(0.0f, 1.0f, 0.0f);
				glm::mat4 view = glm::mat4(1.0f);
				view = glm::lookAt(cameraPos, cameraDirection, cameraUp);

				unsigned int viewLocation = glGetUniformLocation(shaderprogram, "viewTransform");
				glUniformMatrix4fv(viewLocation, 1, GL_FALSE, &view[0][0]);
			}
			else {
				//���� ī�޶�------------------------
				glm::vec3 cameraPos = glm::vec3(c_pos_x_f, body_y, c_pos_z_f);
				glm::vec3 cameraDirection = glm::vec3(0.0f, 0.0f, -50.0f);
				glm::vec3 cameraUp = glm::vec3(0.0f, 1.0f, 0.0f);
				glm::mat4 view = glm::mat4(1.0f);
				view = glm::lookAt(cameraPos, cameraDirection, cameraUp);

				unsigned int viewLocation = glGetUniformLocation(shaderprogram, "viewTransform");
				glUniformMatrix4fv(viewLocation, 1, GL_FALSE, &view[0][0]);
			}

		}

		//���� ����
		glm::mat4 projection = glm::mat4(1.0f);
		projection = glm::perspective(glm::radians(30.0f), (float)800 / (float)800, 0.1f, 100.0f);

		unsigned int projectionLocation = glGetUniformLocation(shaderprogram, "projectionTransform");
		glUniformMatrix4fv(projectionLocation, 1, GL_FALSE, &projection[0][0]);
		//-----------------------------------

		glm::mat4 light_cube = glm::mat4(1.0f);
		glm::vec3 test(light_x, light_y, -light_z);
		light_cube = glm::translate(light_cube, test) *glm::scale(light_cube, glm::vec3(0.2f));
		glm::vec4 test2(0, 0, 0, 1);
		test2 = light_cube * test2;

		//����ť��
		unsigned int modelLocation3 = glGetUniformLocation(shaderprogram, "modelTransform");
		glUniformMatrix4fv(modelLocation3, 1, GL_FALSE, glm::value_ptr(light_cube));
		//-----------------------------------------------------------------


		//����-------------------------------------------------------------------
		int lightPosLocation3 = glGetUniformLocation(shaderprogram, "lightPos"); //--- lightPos ������
		glUniform3f(lightPosLocation3, 1.2, 1.0, 1.0);
		int lightColorLocation3 = glGetUniformLocation(shaderprogram, "lightColor"); //--- lightColor������
		glUniform3f(lightColorLocation3, 1.0f, 1.0f, 1.0f);
		int objColorLocation3 = glGetUniformLocation(shaderprogram, "objectColor"); //--- object Color������
		glUniform3f(objColorLocation3, 1.0f, 1.0f, 1.0f);
		int personLocation3 = glGetUniformLocation(shaderprogram, "viewPos");
		glUniform3f(personLocation3, 0.0f, 0.0f, 3.0f);

		glBindVertexArray(light_vao);
		glDrawArrays(GL_TRIANGLES, 0, 36);

		//���ٴ�
		//------------------------------------------------------------------
		glm::mat4 ground = glm::mat4(1.0f);
		//ground = glm::translate(ground, glm::vec3(0.0f, 0.0f, -3.0f));

		unsigned int modelLocation = glGetUniformLocation(shaderprogram, "modelTransform");
		glUniformMatrix4fv(modelLocation, 1, GL_FALSE, glm::value_ptr(ground));

		//����-------------------------------------------------------------------
		int lightPosLocation = glGetUniformLocation(shaderprogram, "lightPos"); //--- lightPos ������
		glUniform3f(lightPosLocation, test2.x, test2.y, test2.z);
		int lightColorLocation = glGetUniformLocation(shaderprogram, "lightColor"); //--- lightColor������
		glUniform3f(lightColorLocation, 1.0f, 1.0f, 1.0f);
		int objColorLocation = glGetUniformLocation(shaderprogram, "objectColor"); //--- object Color������
		glUniform3f(objColorLocation, ground_color_r, ground_color_g, ground_color_b);
		int personLocation = glGetUniformLocation(shaderprogram, "viewPos");
		glUniform3f(personLocation, 0.0f, 0.0f, 3.0f);

		glBindVertexArray(ground_vao);
		glDrawArrays(GL_TRIANGLES, 0, 36);

		//player---------------------------------------------------------
		glm::mat4 player_move = glm::mat4(1.0f);
		glm::mat4 player_first_state = glm::mat4(1.0f);
		glm::mat4 player_trans = glm::mat4(1.0f);
		glm::mat4 player_rotate_y = glm::mat4(1.0f);

		glm::mat4 player_scale = glm::mat4(1.0f);
		player_scale = glm::scale(player_scale, glm::vec3(0.5f));

		player_first_state = glm::translate(player_first_state, glm::vec3(0.f, -0.25f, -0.f));
		player_rotate_y = glm::rotate(player_rotate_y, glm::radians(player_angle), glm::vec3(0.0f, 1.0f, 0.0f));
		player_trans = glm::translate(player_trans, glm::vec3(body_x, body_y, body_z));

		if (l_pressed == true) {
			player_move = player_trans * player_first_state * player_rotate_y * player_scale;
		}
		else {
			player_move = player_trans * player_first_state * player_rotate_y;
		}


		unsigned int modelLocation2 = glGetUniformLocation(shaderprogram, "modelTransform");
		glUniformMatrix4fv(modelLocation2, 1, GL_FALSE, glm::value_ptr(player_move));

		////-----------------------------------------------------------------
		//unsigned int projectionLocation2 = glGetUniformLocation(shaderprogram, "projectionTransform");
		//glUniformMatrix4fv(projectionLocation2, 1, GL_FALSE, &projection[0][0]);
		//����-------------------------------------------------------------------
		int lightPosLocation2 = glGetUniformLocation(shaderprogram, "lightPos"); //--- lightPos ������
		glUniform3f(lightPosLocation2, test2.x, test2.y, test2.z);
		int lightColorLocation2 = glGetUniformLocation(shaderprogram, "lightColor"); //--- lightColor������
		glUniform3f(lightColorLocation2, 1.0f, 1.0f, 1.0f);
		int objColorLocation2 = glGetUniformLocation(shaderprogram, "objectColor"); //--- object Color������
		glUniform3f(objColorLocation2, 1.0f, 0.0f, 0.0f);
		int personLocation2 = glGetUniformLocation(shaderprogram, "viewPos");
		glUniform3f(personLocation2, 0.0f, 0.0f, 3.0f);

		glBindVertexArray(cube_vao[0]);
		glDrawArrays(GL_TRIANGLES, 0, 36);

		//��ֹ� ����-------------------------------------------------------
		//�⺻ ��ֹ�



		for (obs_iter = obs.begin(); obs_iter != obs.end(); ) {
			obs_iter->make_obs1();
			++obs_iter;
		}

		for (ring_iter = ring_obs.begin(); ring_iter != ring_obs.end(); ) {
			ring_iter->make_obs2();
			++ring_iter;
		}

		//��
		for (oc_iter = oc_obs.begin(); oc_iter != oc_obs.end();) {
			oc_iter->make_obs3();
			++oc_iter;
		}


		for (iter = trees.begin(); iter != trees.end(); ) {
			iter->draw();
			++iter;
		}

		//snow
		for (sn_iter = snow.begin(); sn_iter != snow.end(); ) {
			sn_iter->draw();
			++sn_iter;
		}

		//----------------------------------------------
		glClearColor(0, 0, 0, 1.0f);

		glClear(GL_DEPTH_BUFFER_BIT);

		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

		glUseProgram(shaderprogram_ui);

		glActiveTexture(GL_TEXTURE0);
		glBindTexture(GL_TEXTURE_2D, texture1);

		
		testnum++;
		drawInt(life, -1, 1, 0.1f);
		//drawInt(1203, 0, 0, 0.1f, 0.2f, 0.98f, 0.68f);
		drawInt(testnum / 10, 0.7, 0.7, 0.05f, 1 * (testnum / 1000.f), 1 * (1 - testnum / 1000.f), 0.1f);
		//if (testnum > 1000)testnum = 0;
	}

	

	//-----------------------------------------------
	//���� ���� â

	else if (state == game_over_state) {
		glClearColor(0, 0, 0, 1.0f);

		glClear(GL_DEPTH_BUFFER_BIT);

		glUseProgram(shaderprogram_game_over);

		// ���� ī�޶�------------------------------------------
		glm::vec3 cameraPos_go = glm::vec3(0.0f, 0.0f, 3.5f);
		glm::vec3 cameraDirection_go = glm::vec3(0.0f, 0.0f, 0.0f);
		glm::vec3 cameraUp_go = glm::vec3(0.0f, 1.0f, 0.0f);
		glm::mat4 view_go = glm::mat4(1.0f);
		view_go = glm::lookAt(cameraPos_go, cameraDirection_go, cameraUp_go);

		unsigned int viewLocation_go = glGetUniformLocation(shaderprogram_game_over, "viewTransform");
		glUniformMatrix4fv(viewLocation_go, 1, GL_FALSE, &view_go[0][0]);

		//���� ����
		glm::mat4 projection_go = glm::mat4(1.0f);
		projection_go = glm::perspective(glm::radians(30.0f), (float)800 / (float)800, 0.1f, 100.0f);

		unsigned int projectionLocation_go = glGetUniformLocation(shaderprogram_game_over, "projectionTransform");
		glUniformMatrix4fv(projectionLocation_go, 1, GL_FALSE, &projection_go[0][0]);

		//��
		glm::mat4 game_over = glm::mat4(1.0f);

		unsigned int modelLocation_go = glGetUniformLocation(shaderprogram_game_over, "modelTransform");
		glUniformMatrix4fv(modelLocation_go, 1, GL_FALSE, glm::value_ptr(game_over));


		glBindVertexArray(game_over_vao);

		glActiveTexture(GL_TEXTURE0);
		glBindTexture(GL_TEXTURE_2D, texture_end);

		glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, 0);
	}
	

	//�׸���
	glutSwapBuffers();

}

GLvoid Reshape(int w, int h) // �ݹ� �Լ�: �ٽ� �׸��� 
{
	glViewport(0, 0, w, h);
}



float left_a, bottom_a, back_a, right_a, top_a, front_a = 0;
float left_b, bottom_b, back_b, right_b, top_b, front_b = 0;


void Timerfunction(int value) {

	if (life <= 0) {
		state = game_over_state;
	}

	if (l_pressed) {
		body_bb_x = 0.15f;
	}
	else {
		body_bb_x = 0.25f;
	}

	//-----------------------------------
	//�÷��̾� ������--------------------

	body_x += body_dx;
	body_y += body_dy;
	body_z += body_dz;

	body_dy += gravity;
	//-----------------------------------
	//1��Ī ī�޶� ������
	c_pos_x_f += c_pos_dx_f;
	c_pos_y_f += c_pos_dy_f;
	c_pos_z_f += c_pos_dz_f;

	c_pos_dy_f += gravity;
	//-------------------------------------

	//�÷��̾�&�ٴ� �浹ó��
	if (body_y <= -0.f) {
		body_y = -0.f;
		jumping = false;

	}
	if (body_x <= -0.7f) {
		body_x = -0.7f;
	}
	else if (body_x >= 0.7f) {
		body_x = 0.7f;
	}
	//ī�޶� �浹ó��
	if (c_pos_y_f <= -0.f) {
		c_pos_y_f = -0.f;
		jumping = false;

	}
	if (c_pos_x_f <= -0.7f) {
		c_pos_x_f = -0.7f;
	}
	else if (c_pos_x_f >= 0.7f) {
		c_pos_x_f = 0.7f;
	}

	//�⺻ ��ֹ�
	for (obs_iter = obs.begin(); obs_iter != obs.end();) {
		//cout << obs_iter->get_obs_z() << endl;
		dis_l = sqrt(pow(((body_x - body_bb_x)-obs_iter->get_obs_x()+obs_bb_x), 2)+ pow(((body_y)-obs_iter->get_obs_y()), 2) 
			+ pow(((body_z- body_bb_x)-obs_iter->get_obs_z()+ obs_bb_x), 2));
		dis_r = sqrt(pow(((body_x + body_bb_x) - obs_iter->get_obs_x() - obs_bb_x), 2) + pow(((body_y)-obs_iter->get_obs_y()), 2)
			+ pow(((body_z - body_bb_x) - obs_iter->get_obs_z() + obs_bb_x), 2));


		if (dis_l <= 0.4f || dis_r <=0.4f) {
			cout << "�浹!" << endl;
			life -= 1;
			obs_iter = obs.erase(obs_iter);

			if (life < 0) {
				life = 0;
			}
			
		}
		
		if (obs_iter->update() || life <= 0) {
			obs_iter = obs.erase(obs_iter);
			cout << "����" << endl;

		}
		else {
			++obs_iter;
		}
	}

	
	
	for (ring_iter = ring_obs.begin(); ring_iter != ring_obs.end();) {
		if (ring_iter->update_ring() || life <= 0) {
			ring_iter = ring_obs.erase(ring_iter);
		}
		else {
			++ring_iter;
		}
	}

	//��&��
	for (oc_iter = oc_obs.begin(); oc_iter != oc_obs.end();) {

		dis_oc_lr = sqrt(pow(((body_x - body_bb_x) - oc_iter->get_oc_x() + obs_bb_x), 2) + pow(((body_y)- oc_iter->get_oc_y()), 2)
			+ pow(((body_z - body_bb_x) - oc_iter->get_oc_z() + obs_bb_x), 2));
		dis_oc_rl = sqrt(pow(((body_x + body_bb_x) - oc_iter->get_oc_x2() - obs_bb_x), 2) + pow(((body_y)-oc_iter->get_oc_y2()), 2)
			+ pow(((body_z - body_bb_x) - oc_iter->get_oc_z2() + obs_bb_x), 2));

		if (dis_oc_lr <= 0.4f || dis_oc_rl <= 0.4f) {
			cout << "�浹!oc" << endl;
			life -= 1;
			oc_iter = oc_obs.erase(oc_iter);

			if (life < 0) {
				life = 0;
			}

		}

		if ((oc_iter->update_oc() || oc_iter->update_oc2()) || life <= 0) {
			oc_iter = oc_obs.erase(oc_iter);
		}
		else {
			++oc_iter;
		}
	}


	for (iter = trees.begin(); iter != trees.end();) {
		if (iter->update() || life<=0) {
			iter = trees.erase(iter);
		}
		else {
			++iter;
		}
	}

	t += dt; //�ð��� ������ ���� ��ֹ��� �ٰ��´�.

	if (t % 20 == 0) { //right side trees
		trees.push_back(Tree(1.15f, -50.0f));
	}
	if (t % 20 == 0) { //left side trees
		trees.push_back(Tree(-1.15f, -50.0f));
	}

	if (t % 50 == 0) {
		obs.push_back(Obstacle(uid(dre),-0.25f, -50.0f));
	}
	if (t % 160 == 0) {
		ring_obs.push_back(ring_Obstacle(uid(dre), uid_ring(dre), -50.0f));
	}
	if (t % 270 == 0) {
		oc_obs.push_back(oc_Obstacle(-0.6f, -0.25f, -50.0f, 0.6f, -0.25f, -50.0f));

	}

	//snow
	snow.push_back(Snow(uid_snow_x(dre), uid_snow_y(dre), uid_snow_z(dre)));

	if ((t > 1000 && t < 1500) || (t > 3000 && t < 3500) || (t > 5000 && t < 5500) || (t > 6000 && t < 6500) || (t > 7000 && t < 7500) || (t > 8000 && t < 8500) || (t > 9000 && t < 9500)
		|| (t > 10000 && t < 10500) || (t > 12000 && t < 12500) || (t > 13000 && t < 13500) || (t > 14000 && t < 14500) || (t > 15000 && t < 15500) || (t > 17000 && t < 17500) 
		|| (t > 18000 && t < 18500) || (t > 19000 && t < 20000)) {
		snowing = true;
		//��
		ground_color_r = 1.0f;
		ground_color_g = 0.8f;
		ground_color_b = 0.61f;

		//����
		tree_color_r = 0.7f;
		tree_color_g = 1.0f;
		tree_color_b = 0.7f;

		for (sn_iter = snow.begin(); sn_iter != snow.end();) {
			if (sn_iter->update() || life <= 0)
			{
				sn_iter = snow.erase(sn_iter);
			}
			else {
				++sn_iter;
			}
		}
	}
	else {
		snowing = false;
		//��
		ground_color_r = 1.0f;
		ground_color_g = 0.5f;
		ground_color_b = 0.31f;

		//����
		tree_color_r = 0.0f;
		tree_color_g = 0.8f;
		tree_color_b = 0.0f;
		for (sn_iter = snow.begin(); sn_iter != snow.end();) {

			sn_iter = snow.erase(sn_iter);
		}
	}


	if (r_pressed % 2 == 1) {

		the += 1;
		new_the = (float)(the + 65)*(3.14 / 180);
		light_x = 5.0 * cos(new_the);
		light_y = 5.0 * sin(new_the);
		/*if (p_pressed == true) {
			the -= 1;
		}*/
	}
	if (r_pressed % 2 == 0) {
		the -= 1;
		new_the = (float)(the + 65)*(3.14 / 180);
		light_x = 5.0 * cos(new_the);
		light_y = 5.0 * sin(new_the);
		/*if (p_pressed == true) {
			the += 1;
		}*/
	}

	//------

	glutPostRedisplay();
	glutTimerFunc(10, Timerfunction, 1);

}