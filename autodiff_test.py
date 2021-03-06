import autodiff as ad
import numpy as np

def test_identity():
    x2 = ad.Variable(name = "x2")
    y = x2

    grad_x2, = ad.gradients(y, [x2])

    executor = ad.Executor([y, grad_x2])
    x2_val = 2 * np.ones(3)
    y_val, grad_x2_val= executor.run(feed_dict = {x2 : x2_val})

    assert isinstance(y, ad.Node)
    assert np.array_equal(y_val, x2_val)
    assert np.array_equal(grad_x2_val, np.ones_like(x2_val))

def test_add_by_const():
    x2 = ad.Variable(name = "x2")
    y = 5 + x2

    grad_x2, = ad.gradients(y, [x2])

    executor = ad.Executor([y, grad_x2])
    x2_val = 2 * np.ones(3)
    y_val, grad_x2_val= executor.run(feed_dict = {x2 : x2_val})

    assert isinstance(y, ad.Node)
    assert np.array_equal(y_val, x2_val + 5)
    assert np.array_equal(grad_x2_val, np.ones_like(x2_val))

def test_mul_by_const():
    x2 = ad.Variable(name = "x2")
    y = 5 * x2

    grad_x2, = ad.gradients(y, [x2])

    executor = ad.Executor([y, grad_x2])
    x2_val = 2 * np.ones(3)
    y_val, grad_x2_val= executor.run(feed_dict = {x2 : x2_val})

    assert isinstance(y, ad.Node)
    assert np.array_equal(y_val, x2_val * 5)
    assert np.array_equal(grad_x2_val, np.ones_like(x2_val) * 5)

def test_add_two_vars():
    x2 = ad.Variable(name = "x2")
    x3 = ad.Variable(name = "x3")
    y = x2 + x3

    grad_x2, grad_x3 = ad.gradients(y, [x2, x3])
  
    executor = ad.Executor([y, grad_x2, grad_x3])
    x2_val = 2 * np.ones(3)
    x3_val = 3 * np.ones(3)
    y_val, grad_x2_val, grad_x3_val = executor.run(feed_dict = {x2: x2_val, x3: x3_val})

    assert isinstance(y, ad.Node)
    assert np.array_equal(y_val, x2_val + x3_val)
    assert np.array_equal(grad_x2_val, np.ones_like(x2_val))
    assert np.array_equal(grad_x3_val, np.ones_like(x3_val))

def test_mul_two_vars():
    x2 = ad.Variable(name = "x2")
    x3 = ad.Variable(name = "x3")
    y = x2 * x3
    
    grad_x2, grad_x3 = ad.gradients(y, [x2, x3])

    executor = ad.Executor([y, grad_x2, grad_x3])
    x2_val = 2 * np.ones(3)
    x3_val = 3 * np.ones(3)
    y_val, grad_x2_val, grad_x3_val = executor.run(feed_dict = {x2: x2_val, x3: x3_val})
 
    assert isinstance(y, ad.Node)
    assert np.array_equal(y_val, x2_val * x3_val)
    assert np.array_equal(grad_x2_val, x3_val)
    assert np.array_equal(grad_x3_val, x2_val)

def test_add_mul_mix_1():
    x1 = ad.Variable(name = "x1")
    x2 = ad.Variable(name = "x2")
    x3 = ad.Variable(name = "x3")
    y = x1 + x2 * x3 * x1
    
    grad_x1, grad_x2, grad_x3 = ad.gradients(y, [x1, x2, x3])
   
    executor = ad.Executor([y, grad_x1, grad_x2, grad_x3])
    x1_val = 1 * np.ones(3)
    x2_val = 2 * np.ones(3)
    x3_val = 3 * np.ones(3)
    y_val, grad_x1_val, grad_x2_val, grad_x3_val = executor.run(feed_dict = {x1 : x1_val, x2: x2_val, x3 : x3_val})

    assert isinstance(y, ad.Node)
    assert np.array_equal(y_val, x1_val + x2_val * x3_val)
    assert np.array_equal(grad_x1_val, np.ones_like(x1_val) + x2_val * x3_val)
    assert np.array_equal(grad_x2_val, x3_val * x1_val)
    assert np.array_equal(grad_x3_val, x2_val * x1_val)

def test_add_mul_mix_2():
    x1 = ad.Variable(name = "x1")
    x2 = ad.Variable(name = "x2")
    x3 = ad.Variable(name = "x3")
    x4 = ad.Variable(name = "x4")
    y = x1 + x2 * x3 * x4
    
    grad_x1, grad_x2, grad_x3, grad_x4 = ad.gradients(y, [x1, x2, x3, x4])
   
    executor = ad.Executor([y, grad_x1, grad_x2, grad_x3, grad_x4])
    x1_val = 1 * np.ones(3)
    x2_val = 2 * np.ones(3)
    x3_val = 3 * np.ones(3)
    x4_val = 4 * np.ones(3)
    y_val, grad_x1_val, grad_x2_val, grad_x3_val, grad_x4_val = executor.run(feed_dict = {x1 : x1_val, x2: x2_val, x3 : x3_val, x4 : x4_val})

    assert isinstance(y, ad.Node)
    assert np.array_equal(y_val, x1_val + x2_val * x3_val * x4_val)
    assert np.array_equal(grad_x1_val, np.ones_like(x1_val))
    assert np.array_equal(grad_x2_val, x3_val * x4_val)
    assert np.array_equal(grad_x3_val, x2_val * x4_val)
    assert np.array_equal(grad_x4_val, x2_val * x3_val)

def test_add_mul_mix_3():
    x2 = ad.Variable(name = "x2")
    x3 = ad.Variable(name = "x3")
    z = x2 * x2 + x2 + x3 + 3
    y = z * z + x3
    
    grad_x2, grad_x3 = ad.gradients(y, [x2, x3])

    executor = ad.Executor([y, grad_x2, grad_x3])
    x2_val = 2 * np.ones(3)
    x3_val = 3 * np.ones(3)
    y_val, grad_x2_val, grad_x3_val = executor.run(feed_dict = {x2: x2_val, x3: x3_val})

    z_val = x2_val * x2_val + x2_val + x3_val + 3
    expected_yval = z_val * z_val + x3_val
    expected_grad_x2_val = 2 * (x2_val * x2_val + x2_val + x3_val + 3) * (2 * x2_val + 1)
    expected_grad_x3_val = 2 * (x2_val * x2_val + x2_val + x3_val + 3) + 1
    assert isinstance(y, ad.Node)
    assert np.array_equal(y_val, expected_yval)
    assert np.array_equal(grad_x2_val, expected_grad_x2_val)
    assert np.array_equal(grad_x3_val, expected_grad_x3_val)

def test_grad_of_grad():
    x2 = ad.Variable(name = "x2")
    x3 = ad.Variable(name = "x3")
    y = x2 * x2 + x2 * x3
    
    grad_x2, grad_x3 = ad.gradients(y, [x2, x3])
    grad_x2_x2, grad_x2_x3 = ad.gradients(grad_x2, [x2, x3])

    executor = ad.Executor([y, grad_x2, grad_x3, grad_x2_x2, grad_x2_x3])
    x2_val = 2 * np.ones(3)
    x3_val = 3 * np.ones(3)
    y_val, grad_x2_val, grad_x3_val, grad_x2_x2_val, grad_x2_x3_val = executor.run(feed_dict = {x2: x2_val, x3: x3_val})

    expected_yval = x2_val * x2_val + x2_val * x3_val
    expected_grad_x2_val = 2 * x2_val + x3_val 
    expected_grad_x3_val = x2_val
    expected_grad_x2_x2_val = 2 * np.ones_like(x2_val)
    expected_grad_x2_x3_val = 1 * np.ones_like(x2_val)

    assert isinstance(y, ad.Node)
    assert np.array_equal(y_val, expected_yval)
    assert np.array_equal(grad_x2_val, expected_grad_x2_val)
    assert np.array_equal(grad_x3_val, expected_grad_x3_val)
    assert np.array_equal(grad_x2_x2_val, expected_grad_x2_x2_val)
    assert np.array_equal(grad_x2_x3_val, expected_grad_x2_x3_val)

def test_matmul_two_vars():
    x2 = ad.Variable(name = "x2")
    x3 = ad.Variable(name = "x3")
    y = ad.matmul_op(x2, x3)

    grad_x2, grad_x3 = ad.gradients(y, [x2, x3])
    
    executor = ad.Executor([y, grad_x2, grad_x3])
    x2_val = np.array([[1, 2], [3, 4], [5, 6]]) # 3x2
    x3_val = np.array([[7, 8, 9], [10, 11, 12]]) # 2x3

    y_val, grad_x2_val, grad_x3_val = executor.run(feed_dict = {x2: x2_val, x3: x3_val})

    expected_yval = np.matmul(x2_val, x3_val)
    expected_grad_x2_val = np.matmul(np.ones_like(expected_yval), np.transpose(x3_val))
    expected_grad_x3_val = np.matmul(np.transpose(x2_val), np.ones_like(expected_yval))

    assert isinstance(y, ad.Node)
    assert np.array_equal(y_val, expected_yval)
    assert np.array_equal(grad_x2_val, expected_grad_x2_val)
    assert np.array_equal(grad_x3_val, expected_grad_x3_val)

def test_logistic_regression_1():
    x = ad.Variable(name = "input")  #n*1
    w = ad.Variable(name = "weight") #n*1
    b = ad.Variable(name = "bias")   #1
    logits = ad.dot_op(w, x) + b
    y = ad.sigmoid_op(logits)

    x_val = 2 * np.ones(3)
    w_val = 3 * np.ones(3)
    b_val = 4

    # executor = ad.Executor([y])
    # y_val, = executor.run(feed_dict = {x: x_val, w: w_val, b: b_val}) #逗号使结果不为list
    # expected_yval = np.divide(1, 1 + np.exp(-(np.dot(x_val, w_val) + b_val)))
    # assert np.array_equal(y_val, expected_yval)
    grad_x, grad_w, grad_b = ad.gradients(y, [x, w, b])
    executor = ad.Executor([y, grad_x, grad_w, grad_b])
    y_val, grad_x_val, grad_w_val, grad_b_val = \
        executor.run(feed_dict = {x: x_val, w: w_val, b: b_val})
    print(grad_x.name, grad_w.name, grad_b.name)
    expected_yval = np.divide(1, 1 + np.exp(-(np.dot(x_val, w_val) + b_val)))
    y_base = np.ones_like(expected_yval)
    expected_grad_x_val = np.multiply(y_base*expected_yval*(1-expected_yval), w_val)
    expected_grad_w_val = np.multiply(y_base*expected_yval*(1-expected_yval), x_val)
    expected_grad_b_val = y_base*expected_yval*(1-expected_yval)

    assert isinstance(y, ad.Node)
    assert np.array_equal(y_val, expected_yval)
    assert np.array_equal(grad_x_val, expected_grad_x_val)
    assert np.array_equal(grad_w_val, expected_grad_w_val)
    assert np.array_equal(grad_b_val, expected_grad_b_val)

def training_loop():
    x = ad.Variable(name = "input")  #n*1
    w = ad.Variable(name = "weight") #n*1
    b = ad.Variable(name = "bias")   #1
    logits = ad.dot_op(w, x) + b
    y = ad.sigmoid_op(logits)
    x_val = 2 * np.ones(3)
    w_val = 3 * np.ones(3)
    b_val = 4

    grad_x, grad_w, grad_b = ad.gradients(y, [x, w, b])
    executor = ad.Executor([y, grad_x, grad_w, grad_b])
    epochs = 10
    learning_rate = 10
    for iter_ in range(epochs):
        print("eposh: %s, weight: %s, bias: %s" % (iter_, w_val, b_val))
        y_val, grad_x_val, grad_w_val, grad_b_val = \
            executor.run(feed_dict = {x: x_val, w: w_val, b: b_val})
        # update parameters 
        w_val = w_val - learning_rate * grad_w_val
        b_val = b_val - learning_rate * grad_b_val
        print(" error:%s, weight-diff:%s, bias-diff:%s" % (grad_x_val, grad_w_val, grad_b_val))

def test_logistic_regression_2():
    x = ad.Variable(name = "input")  #n*1
    w = ad.Variable(name = "weight") #n*1
    b = ad.Variable(name = "bias")   #1
    logits = ad.matmul_op(x, w) + b
    y = ad.softmax_with_cross_entropy_op(logits)

    x_val = np.array([[2, 2, 2]])
    w_val = np.array([[1, 1, 1], [2, 2, 2]]).transpose()
    b_val = 5 * np.ones(2)
    # print(x_val, w_val, b_val, np.matmul(x_val, w_val) + b_val)

    grad_x, grad_w, grad_b = ad.gradients(y, [x, w, b])
    executor = ad.Executor([y, grad_x, grad_w, grad_b])
    y_val, grad_x_val, grad_w_val, grad_b_val = \
        executor.run(feed_dict = {x: x_val, w: w_val, b: b_val})

    x_row_max = (np.dot(x_val, w_val) + b_val).max(axis=-1)
    x_row_max = x_row_max.reshape(list((np.matmul(x_val, w_val) + b_val).shape)[:-1]+[1])
    e_x = np.exp((np.matmul(x_val, w_val) + b_val) - x_row_max)
    expected_yval = e_x / e_x.sum(axis=-1).reshape(list((np.matmul(x_val, w_val) + b_val).shape)[:-1]+[1])
    y_base = np.ones_like(expected_yval)
    expected_grad_x_val = np.matmul(y_base*(expected_yval - 1), w_val.transpose())
    expected_grad_w_val = np.matmul(x_val.transpose(), y_base*(expected_yval - 1))
    expected_grad_b_val = y_base*(expected_yval - 1)
    # print(grad_b_val)
    # print(expected_grad_b_val)
    assert isinstance(y, ad.Node)
    assert np.array_equal(y_val, expected_yval)
    assert np.array_equal(grad_x_val, expected_grad_x_val)
    assert np.array_equal(grad_w_val, expected_grad_w_val)
    assert np.array_equal(grad_b_val, expected_grad_b_val)

if __name__ == '__main__':
    training_loop()