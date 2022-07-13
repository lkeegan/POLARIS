#include "MathFunctions.h"

void CRandomGenerator::init(ullong seed)
{
    generator.seed(seed);
}

double CRandomGenerator::getRND()
{
    return std::uniform_real_distribution<double>{0.0, 1.0}(generator);
}

double CRandomGenerator::getRNDnormal(double mu, double sigma)
{
    return std::normal_distribution<double>{mu, sigma}(generator);
}